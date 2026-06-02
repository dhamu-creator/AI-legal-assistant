"""
PDF Loader for Legal Documents
Extracts text and metadata from legal PDFs with proper handling of multi-column layouts and legal document structures.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

import fitz  # PyMuPDF
import pdfplumber
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LegalDocumentMetadata:
    """Metadata for legal documents"""
    case_name: str
    court_name: str
    judgment_date: Optional[str]
    citation: Optional[str]  # e.g., "[2023] SCC 45"
    judges: List[str]
    ipc_sections: List[str]
    document_source: str
    file_name: str
    total_pages: int
    extraction_date: str


@dataclass
class LegalDocument:
    """Complete legal document with text and metadata"""
    metadata: LegalDocumentMetadata
    full_text: str
    page_contents: List[Dict]  # List of {"page_num": int, "text": str}


class LegalPDFLoader:
    """
    Loader for legal PDFs with specialized handling for Indian court judgments.
    Supports extracting case metadata, judgment text, and IPC section references.
    """

    def __init__(self, pdf_path: str):
        """
        Initialize the PDF loader.
        
        Args:
            pdf_path: Path to the PDF file
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    def extract_text_with_pymupdf(self) -> Tuple[str, List[Dict]]:
        """
        Extract text from PDF using PyMuPDF with layout preservation.
        
        Returns:
            Tuple of (full_text, page_contents)
        """
        full_text = []
        page_contents = []

        try:
            doc = fitz.open(self.pdf_path)
            logger.info(f"Opened PDF: {self.pdf_path.name} ({doc.page_count} pages)")

            for page_num, page in enumerate(doc):
                # Extract text with layout information
                text = page.get_text("text")
                
                # Handle multi-column layouts - try to detect and reorder
                text = self._handle_multicolumn_layout(text)
                
                full_text.append(text)
                page_contents.append({
                    "page_num": page_num + 1,
                    "text": text,
                    "page_height": page.rect.height,
                    "page_width": page.rect.width
                })

            doc.close()
            return "\n\n".join(full_text), page_contents

        except Exception as e:
            logger.error(f"Error extracting text with PyMuPDF: {str(e)}")
            raise

    def extract_text_with_pdfplumber(self) -> Tuple[str, List[Dict]]:
        """
        Extract text from PDF using pdfplumber as fallback/enrichment.
        Useful for extracting tables and maintaining structure.
        
        Returns:
            Tuple of (full_text, page_contents)
        """
        full_text = []
        page_contents = []

        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                logger.info(f"Opened PDF with pdfplumber: {self.pdf_path.name} ({len(pdf.pages)} pages)")

                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    
                    # Extract tables if present
                    tables = page.extract_tables()
                    if tables:
                        text += "\n\n[TABLES IN DOCUMENT]\n"
                        for table in tables:
                            text += self._format_table(table) + "\n"
                    
                    full_text.append(text)
                    page_contents.append({
                        "page_num": page_num + 1,
                        "text": text,
                        "has_tables": bool(tables)
                    })

            return "\n\n".join(full_text), page_contents

        except Exception as e:
            logger.error(f"Error extracting text with pdfplumber: {str(e)}")
            raise

    def extract_text(self, use_pdfplumber: bool = False) -> Tuple[str, List[Dict]]:
        """
        Extract text from PDF (uses PyMuPDF by default, falls back to pdfplumber).
        
        Args:
            use_pdfplumber: If True, use pdfplumber; otherwise use PyMuPDF
        
        Returns:
            Tuple of (full_text, page_contents)
        """
        if use_pdfplumber:
            return self.extract_text_with_pdfplumber()
        else:
            return self.extract_text_with_pymupdf()

    def extract_case_metadata(self, text: str) -> Dict:
        """
        Extract case metadata from the document text using regex patterns.
        
        Args:
            text: Full extracted text from PDF
        
        Returns:
            Dictionary containing extracted metadata
        """
        metadata = {
            "case_name": None,
            "court_name": None,
            "judgment_date": None,
            "citation": None,
            "judges": [],
            "ipc_sections": []
        }

        # Extract case name (typically at the beginning)
        case_match = re.search(r"(?:In the matter of|Case No\.|Civil Case|Criminal Case|Appeal No\.)\s+([^\n]+)", text, re.IGNORECASE)
        if case_match:
            metadata["case_name"] = case_match.group(1).strip()

        # Extract court name
        court_patterns = [
            r"Supreme Court of India",
            r"High Court of (\w+)",
            r"District Court",
            r"Court of (\w+)"
        ]
        for pattern in court_patterns:
            court_match = re.search(pattern, text, re.IGNORECASE)
            if court_match:
                metadata["court_name"] = court_match.group(0).strip()
                break

        # Extract judgment date (common formats: DD/MM/YYYY, DD.MM.YYYY, etc.)
        date_match = re.search(r"(?:Judgment|\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})", text)
        if date_match:
            metadata["judgment_date"] = date_match.group(0).strip()

        # Extract case citation (e.g., [2023] SCC 45, AIR 2021 SC 123)
        citation_pattern = r"\[\d{4}\]\s+(?:SCC|SC|HC|AIR|SCR)\s+\d+"
        citations = re.findall(citation_pattern, text)
        if citations:
            metadata["citation"] = citations[0]

        # Extract judge names (typically preceded by "By" or "Delivered by")
        judge_pattern = r"(?:By|Delivered by|J\.|Judgment by)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:J\.|CJ|SCJ)"
        judges = re.findall(judge_pattern, text)
        if judges:
            metadata["judges"] = list(set(judges))[:5]  # Limit to 5 unique judges

        # Extract IPC sections
        ipc_pattern = r"(?:Section|§|S\.|Sec\.)\s+(\d+)\s+(?:IPC|of the Indian Penal Code)"
        ipc_sections = re.findall(ipc_pattern, text, re.IGNORECASE)
        if ipc_sections:
            metadata["ipc_sections"] = list(set(ipc_sections))

        return metadata

    def load_document(self) -> LegalDocument:
        """
        Load a complete legal document with text and metadata.
        
        Returns:
            LegalDocument object with full content and metadata
        """
        logger.info(f"Loading document: {self.pdf_path.name}")

        # Extract text
        full_text, page_contents = self.extract_text()

        # Try secondary extraction for enrichment
        try:
            _, page_contents_secondary = self.extract_text(use_pdfplumber=True)
            logger.info("Secondary extraction with pdfplumber completed")
        except Exception as e:
            logger.warning(f"Secondary extraction failed: {str(e)}")
            page_contents_secondary = page_contents

        # Extract metadata
        raw_metadata = self.extract_case_metadata(full_text)

        # Create metadata object
        metadata = LegalDocumentMetadata(
            case_name=raw_metadata.get("case_name", "Unknown Case"),
            court_name=raw_metadata.get("court_name", "Unknown Court"),
            judgment_date=raw_metadata.get("judgment_date"),
            citation=raw_metadata.get("citation"),
            judges=raw_metadata.get("judges", []),
            ipc_sections=raw_metadata.get("ipc_sections", []),
            document_source=self.pdf_path.name,
            file_name=self.pdf_path.stem,
            total_pages=len(page_contents),
            extraction_date=datetime.now().isoformat()
        )

        legal_doc = LegalDocument(
            metadata=metadata,
            full_text=full_text,
            page_contents=page_contents
        )

        logger.info(f"Successfully loaded: {legal_doc.metadata.case_name}")
        logger.info(f"  Court: {legal_doc.metadata.court_name}")
        logger.info(f"  Citation: {legal_doc.metadata.citation}")
        logger.info(f"  IPC Sections: {', '.join(legal_doc.metadata.ipc_sections)}")

        return legal_doc

    def save_to_json(self, output_path: str) -> None:
        """
        Save document to JSON format for processing.
        
        Args:
            output_path: Path where JSON should be saved
        """
        doc = self.load_document()
        
        output_data = {
            "metadata": asdict(doc.metadata),
            "full_text": doc.full_text,
            "page_contents": doc.page_contents
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved document to: {output_path}")

    @staticmethod
    def _handle_multicolumn_layout(text: str) -> str:
        """
        Handle multi-column PDF layouts by detecting and reordering columns.
        This is a basic approach; advanced layouts may need specialized processing.
        
        Args:
            text: Extracted text potentially in multi-column format
        
        Returns:
            Reordered text
        """
        # Simple heuristic: if line lengths vary significantly, might be multi-column
        # For now, return as-is; can be enhanced with advanced column detection
        return text

    @staticmethod
    def _format_table(table: List[List]) -> str:
        """
        Format extracted table as readable text.
        
        Args:
            table: Table extracted by pdfplumber
        
        Returns:
            Formatted table as string
        """
        if not table:
            return ""
        
        formatted = []
        for row in table:
            formatted.append(" | ".join(str(cell) if cell else "" for cell in row))
        
        return "\n".join(formatted)


def batch_load_pdfs(pdf_directory: str, output_directory: str) -> List[str]:
    """
    Batch load multiple PDFs from a directory and save as JSON.
    
    Args:
        pdf_directory: Directory containing PDF files
        output_directory: Directory to save JSON outputs
    
    Returns:
        List of successfully processed file paths
    """
    pdf_dir = Path(pdf_directory)
    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    processed_files = []

    for pdf_file in pdf_dir.glob("*.pdf"):
        try:
            loader = LegalPDFLoader(str(pdf_file))
            output_json = output_dir / f"{pdf_file.stem}.json"
            loader.save_to_json(str(output_json))
            processed_files.append(str(output_json))
        except Exception as e:
            logger.error(f"Failed to process {pdf_file.name}: {str(e)}")

    logger.info(f"Batch processing complete. Processed {len(processed_files)} files.")
    return processed_files


if __name__ == "__main__":
    # Example usage
    pdf_path = "sample_judgement.pdf"
    
    try:
        loader = LegalPDFLoader(pdf_path)
        doc = loader.load_document()
        
        print("\n" + "="*50)
        print(f"Case: {doc.metadata.case_name}")
        print(f"Court: {doc.metadata.court_name}")
        print(f"Citation: {doc.metadata.citation}")
        print(f"Date: {doc.metadata.judgment_date}")
        print(f"Judges: {', '.join(doc.metadata.judges)}")
        print(f"IPC Sections: {', '.join(doc.metadata.ipc_sections)}")
        print("="*50)
        print(f"\nFirst 500 characters:\n{doc.full_text[:500]}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
