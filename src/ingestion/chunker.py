"""
Smart Legal Document Chunker
Chunks legal documents intelligently while preserving legal context and references.
"""

import re
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LegalChunk:
    """Represents a chunk of legal text with associated metadata"""
    chunk_id: str
    text: str
    source_file: str
    case_name: str
    court_name: str
    page_numbers: List[int]
    ipc_sections: List[str]
    case_citations: List[str]
    chunk_type: str  # "judgment", "section", "argument", "order"
    context_window: Optional[str] = None  # Surrounding text for context
    start_position: int = 0
    end_position: int = 0


class LegalDocumentChunker:
    """
    Intelligent chunker for legal documents that preserves legal context.
    """

    # Legal document section markers
    SECTION_PATTERNS = {
        "heading": r"^[A-Z\s\d\-\.]+:?$",
        "section": r"^(?:Section|§|S\.|Sec\.)\s+\d+[A-Z]?\.?",
        "article": r"^(?:Article|Art\.)\s+\d+[A-Z]?\.?",
        "subsection": r"^\s+\(\d+\)\s+",
        "schedule": r"^(?:Schedule|SCHEDULE)",
        "order": r"^(?:ORDERED|ORDER)",
        "date": r"^\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
    }

    # IPC section pattern
    IPC_PATTERN = r"(?:Section|§|S\.|Sec\.)\s+(\d+)\s+(?:IPC|of the Indian Penal Code)"
    
    # Case citation patterns
    CITATION_PATTERNS = [
        r"\[\d{4}\]\s+(?:SCC|SCR|SCJ|ALJ|AIR|HC)\s+\d+",  # [2023] SCC 45
        r"(?:AIR|SCC|SCR)\s+\d{4}\s+(?:SC|HC)\s+\d+",     # AIR 2021 SC 123
        r"\d+\s+(?:SCC|SCR|AIR)\s+\d+",                     # 2023 SCC Online 45
    ]

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
        preserve_sections: bool = True,
        min_chunk_size: int = 20
    ):
        """
        Initialize the chunker.
        
        Args:
            chunk_size: Target number of words per chunk
            chunk_overlap: Number of words to overlap between chunks
            preserve_sections: If True, don't split within legal sections
            min_chunk_size: Minimum words for a valid chunk
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.preserve_sections = preserve_sections
        self.min_chunk_size = min_chunk_size

    def chunk_document(
        self,
        text: str,
        metadata: Dict,
        page_contents: Optional[List[Dict]] = None
    ) -> List[LegalChunk]:
        """
        Chunk a legal document while preserving context and legal structure.
        
        Args:
            text: Full document text
            metadata: Document metadata (case_name, court_name, etc.)
            page_contents: List of page-by-page content for page tracking
        
        Returns:
            List of LegalChunk objects
        """
        logger.info(f"Chunking document: {metadata.get('case_name', 'Unknown')}")

        # Split into sentences first
        sentences = self._split_into_sentences(text)
        
        # Group sentences into sections if preserve_sections is True
        if self.preserve_sections:
            sections = self._identify_legal_sections(sentences)
            chunks = self._chunk_sections(sections, metadata)
        else:
            chunks = self._chunk_sentences(sentences, metadata)

        # Extract IPC sections and citations for each chunk
        for chunk in chunks:
            chunk.ipc_sections = self._extract_ipc_sections(chunk.text)
            chunk.case_citations = self._extract_citations(chunk.text)
            chunk.page_numbers = self._map_chunk_to_pages(chunk, page_contents)

        logger.info(f"Created {len(chunks)} chunks from document")
        return chunks

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences while preserving legal references.
        
        Args:
            text: Input text
        
        Returns:
            List of sentences
        """
        # Replace common abbreviations to prevent sentence splitting
        text = re.sub(r'\bNo\.\s+', 'No_', text)
        text = re.sub(r'\bvol\.\s+', 'Vol_', text)
        text = re.sub(r'\bpp\.\s+', 'pp_', text)
        text = re.sub(r'\bSec\.\s+', 'Sec_', text)
        text = re.sub(r'\bA\.I\.R\.\s+', 'AIR_', text)
        text = re.sub(r'\bS\.C\.C\.\s+', 'SCC_', text)

        # Split by period, exclamation, question mark (with lookahead)
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)

        # Restore abbreviations
        sentences = [
            s.replace('No_', 'No. ')
            .replace('Vol_', 'vol. ')
            .replace('pp_', 'pp. ')
            .replace('Sec_', 'Sec. ')
            .replace('AIR_', 'A.I.R. ')
            .replace('SCC_', 'S.C.C. ')
            for s in sentences
        ]

        return [s.strip() for s in sentences if s.strip()]

    def _identify_legal_sections(self, sentences: List[str]) -> List[Dict]:
        """
        Identify and group sentences into legal sections.
        
        Args:
            sentences: List of sentences
        
        Returns:
            List of sections with sentences grouped together
        """
        sections = []
        current_section = {
            "type": "body",
            "sentences": [],
            "headers": []
        }

        for sentence in sentences:
            # Check if this sentence is a section header
            for section_type, pattern in self.SECTION_PATTERNS.items():
                if re.match(pattern, sentence, re.MULTILINE):
                    # Save previous section
                    if current_section["sentences"]:
                        sections.append(current_section)
                    
                    # Start new section
                    current_section = {
                        "type": section_type,
                        "sentences": [sentence],
                        "headers": [sentence]
                    }
                    break
            else:
                # Regular sentence - add to current section
                current_section["sentences"].append(sentence)

        # Don't forget the last section
        if current_section["sentences"]:
            sections.append(current_section)

        logger.debug(f"Identified {len(sections)} sections")
        return sections

    def _chunk_sections(self, sections: List[Dict], metadata: Dict) -> List[LegalChunk]:
        """
        Chunk content while respecting section boundaries.
        
        Args:
            sections: Identified legal sections
            metadata: Document metadata
        
        Returns:
            List of LegalChunk objects
        """
        chunks = []
        chunk_id_counter = 0
        overlap_buffer = []

        for section_idx, section in enumerate(sections):
            section_text = " ".join(section["sentences"])
            words = section_text.split()

            # If section is smaller than chunk_size, keep it as single chunk
            if len(words) <= self.chunk_size:
                chunk_id = f"{metadata.get('file_name', 'doc')}_s{section_idx}_c{chunk_id_counter}"
                chunk_text = section_text

                if chunk_text.split().__len__() >= self.min_chunk_size:
                    chunk = LegalChunk(
                        chunk_id=chunk_id,
                        text=chunk_text,
                        source_file=metadata.get('file_name', 'unknown'),
                        case_name=metadata.get('case_name', 'Unknown'),
                        court_name=metadata.get('court_name', 'Unknown'),
                        page_numbers=[],
                        ipc_sections=[],
                        case_citations=[],
                        chunk_type=section.get("type", "body"),
                        start_position=0,
                        end_position=len(section_text)
                    )
                    chunks.append(chunk)
                    chunk_id_counter += 1
            else:
                # Break large sections into chunks with overlap
                chunk_start = 0
                chunk_num = 0

                while chunk_start < len(words):
                    chunk_end = min(chunk_start + self.chunk_size, len(words))
                    chunk_words = words[chunk_start:chunk_end]
                    chunk_text = " ".join(chunk_words)

                    if len(chunk_words) >= self.min_chunk_size:
                        chunk_id = f"{metadata.get('file_name', 'doc')}_s{section_idx}_c{chunk_num}"
                        
                        chunk = LegalChunk(
                            chunk_id=chunk_id,
                            text=chunk_text,
                            source_file=metadata.get('file_name', 'unknown'),
                            case_name=metadata.get('case_name', 'Unknown'),
                            court_name=metadata.get('court_name', 'Unknown'),
                            page_numbers=[],
                            ipc_sections=[],
                            case_citations=[],
                            chunk_type=section.get("type", "body"),
                            start_position=chunk_start,
                            end_position=chunk_end
                        )
                        chunks.append(chunk)
                        chunk_num += 1

                    # Move forward with overlap
                    chunk_start += self.chunk_size - self.chunk_overlap

        return chunks

    def _chunk_sentences(self, sentences: List[str], metadata: Dict) -> List[LegalChunk]:
        """
        Simple chunking based on sentence count (fallback method).
        
        Args:
            sentences: List of sentences
            metadata: Document metadata
        
        Returns:
            List of LegalChunk objects
        """
        chunks = []
        chunk_id_counter = 0

        # Convert sentences to words and chunk
        words = []
        sentence_boundaries = [0]  # Track where each sentence starts/ends

        for sentence in sentences:
            words.extend(sentence.split())
            sentence_boundaries.append(len(words))

        chunk_start_idx = 0
        while chunk_start_idx < len(words):
            chunk_end_idx = min(chunk_start_idx + self.chunk_size, len(words))
            chunk_words = words[chunk_start_idx:chunk_end_idx]
            chunk_text = " ".join(chunk_words)

            if len(chunk_words) >= self.min_chunk_size:
                chunk_id = f"{metadata.get('file_name', 'doc')}_c{chunk_id_counter}"
                
                chunk = LegalChunk(
                    chunk_id=chunk_id,
                    text=chunk_text,
                    source_file=metadata.get('file_name', 'unknown'),
                    case_name=metadata.get('case_name', 'Unknown'),
                    court_name=metadata.get('court_name', 'Unknown'),
                    page_numbers=[],
                    ipc_sections=[],
                    case_citations=[],
                    chunk_type="body",
                    start_position=chunk_start_idx,
                    end_position=chunk_end_idx
                )
                chunks.append(chunk)
                chunk_id_counter += 1

            chunk_start_idx += self.chunk_size - self.chunk_overlap

        return chunks

    def _extract_ipc_sections(self, text: str) -> List[str]:
        """
        Extract IPC section references from text.
        
        Args:
            text: Chunk text
        
        Returns:
            List of IPC sections found
        """
        ipc_sections = []
        matches = re.finditer(self.IPC_PATTERN, text, re.IGNORECASE)
        
        for match in matches:
            section_num = match.group(1)
            ipc_sections.append(f"Section {section_num}")

        return list(set(ipc_sections))

    def _extract_citations(self, text: str) -> List[str]:
        """
        Extract case citations from text.
        
        Args:
            text: Chunk text
        
        Returns:
            List of case citations found
        """
        citations = []
        
        for pattern in self.CITATION_PATTERNS:
            matches = re.finditer(pattern, text)
            for match in matches:
                citations.append(match.group(0))

        return list(set(citations))

    def _map_chunk_to_pages(
        self,
        chunk: LegalChunk,
        page_contents: Optional[List[Dict]]
    ) -> List[int]:
        """
        Map chunk position to page numbers.
        
        Args:
            chunk: LegalChunk object
            page_contents: List of page contents from PDF
        
        Returns:
            List of page numbers
        """
        if not page_contents:
            return [1]  # Default to first page

        # Simple heuristic: based on position in document
        total_chars = sum(len(page.get('text', '')) for page in page_contents)
        
        if total_chars == 0:
            return [1]

        char_position = int((chunk.start_position / 1000) * total_chars)  # Approximate
        current_pos = 0

        for page_info in page_contents:
            page_text_len = len(page_info.get('text', ''))
            if current_pos + page_text_len >= char_position:
                return [page_info.get('page_num', 1)]
            current_pos += page_text_len

        return [len(page_contents)]

    @staticmethod
    def chunks_to_json(chunks: List[LegalChunk], output_path: str) -> None:
        """
        Save chunks to JSON file for ingestion into vector database.
        
        Args:
            chunks: List of LegalChunk objects
            output_path: Output JSON file path
        """
        chunks_data = [asdict(chunk) for chunk in chunks]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chunks_data, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved {len(chunks)} chunks to {output_path}")


def chunk_legal_documents_batch(
    json_directory: str,
    output_directory: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> Dict[str, List[LegalChunk]]:
    """
    Batch chunk multiple legal documents from JSON files.
    
    Args:
        json_directory: Directory containing extracted JSON files
        output_directory: Directory to save chunked output
        chunk_size: Words per chunk
        chunk_overlap: Overlap in words
    
    Returns:
        Dictionary mapping file names to chunks
    """
    json_dir = Path(json_directory)
    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    chunker = LegalDocumentChunker(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    all_chunks = {}

    for json_file in json_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                doc_data = json.load(f)

            metadata = doc_data.get('metadata', {})
            text = doc_data.get('full_text', '')
            page_contents = doc_data.get('page_contents', [])

            chunks = chunker.chunk_document(text, metadata, page_contents)
            all_chunks[json_file.stem] = chunks

            # Save chunks
            output_json = output_dir / f"{json_file.stem}_chunks.json"
            chunker.chunks_to_json(chunks, str(output_json))

        except Exception as e:
            logger.error(f"Failed to chunk {json_file.name}: {str(e)}")

    logger.info(f"Batch chunking complete. Processed {len(all_chunks)} documents.")
    return all_chunks


if __name__ == "__main__":
    # Example usage
    json_path = "sample_data.json"
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            doc_data = json.load(f)

        metadata = doc_data.get('metadata', {})
        text = doc_data.get('full_text', '')
        page_contents = doc_data.get('page_contents', [])

        chunker = LegalDocumentChunker(chunk_size=500, chunk_overlap=100)
        chunks = chunker.chunk_document(text, metadata, page_contents)

        print(f"\nCreated {len(chunks)} chunks\n")
        for i, chunk in enumerate(chunks[:3]):
            print(f"Chunk {i+1}:")
            print(f"  ID: {chunk.chunk_id}")
            print(f"  Type: {chunk.chunk_type}")
            print(f"  Text: {chunk.text[:100]}...")
            print(f"  IPC: {chunk.ipc_sections}")
            print(f"  Citations: {chunk.case_citations}")
            print()

    except Exception as e:
        print(f"Error: {str(e)}")
