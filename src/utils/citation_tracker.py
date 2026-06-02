"""
Citation Tracking and Formatting
Extracts, formats, and manages legal citations in documents and responses.
"""

import re
import json
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CitationType(Enum):
    """Types of legal citations"""
    IPC_SECTION = "ipc_section"
    CASE = "case"
    ACT = "act"
    ARTICLE = "article"
    RULE = "rule"
    SCHEDULE = "schedule"
    AMENDMENT = "amendment"


@dataclass
class Citation:
    """Structured citation object"""
    type: CitationType
    citation_text: str
    year: Optional[int] = None
    number: Optional[str] = None
    reporter: Optional[str] = None
    context: Optional[str] = None  # Surrounding text


class CitationExtractor:
    """
    Extracts various types of legal citations from text.
    """

    # Regex patterns for different citation types
    PATTERNS = {
        "ipc_section": r"(?:Section|§|S\.)\s+(\d+[A-Z]?(?:\-[A-Z])?)(?:\s+(?:IPC|of the Indian Penal Code))?",
        "case_scc": r"\[\s*(\d{4})\s*\]\s+SCC\s+(\d+)",  # [2021] SCC 45
        "case_air": r"AIR\s+(\d{4})\s+(\w+)\s+(\d+)",   # AIR 2021 SC 123
        "case_scr": r"\[\s*(\d{4})\s*\]\s+SCR\s+(\d+)",  # [2021] SCR 45
        "case_generic": r"\[\s*(\d{4})\s*\]\s+(\w+)\s+(\d+)",  # Generic [YYYY] REPORTER PAGE
        "constitution": r"(?:of the\s+)?Constitution(?:\s+of India)?(?:\s+)?(?:Article|Art\.)\s+(\d+)",
        "article": r"Article\s+(\d+)(?:\s+of the\s+)?(?:Constitution)?",
        "acts": r"(?:the\s+)?([A-Z][a-zA-Z\s&]+?)(?:Act|Code)(?:\s+of\s+\d{4})?(?:\s+\(|\s+,|\s+as|\s+for|$)",
        "rules": r"Rule\s+(\d+)",
        "order": r"Order\s+(\d+)",
        "schedule": r"Schedule\s+([IVX]+)",
        "amendment": r"(\d+)(?:st|nd|rd|th)?\s+Amendment"
    }

    def __init__(self):
        """Initialize extractor with compiled patterns."""
        self.compiled_patterns = {
            key: re.compile(pattern, re.IGNORECASE)
            for key, pattern in self.PATTERNS.items()
        }

    def extract_all(self, text: str) -> Dict[str, List[Citation]]:
        """
        Extract all types of citations from text.
        
        Args:
            text: Text to extract citations from
        
        Returns:
            Dictionary mapping citation types to lists of Citation objects
        """
        citations = {
            "ipc_sections": self._extract_ipc_sections(text),
            "cases": self._extract_cases(text),
            "acts": self._extract_acts(text),
            "articles": self._extract_articles(text),
            "rules": self._extract_rules(text),
            "schedules": self._extract_schedules(text),
            "amendments": self._extract_amendments(text)
        }
        
        return citations

    def _extract_ipc_sections(self, text: str) -> List[Citation]:
        """Extract IPC section citations."""
        citations = []
        
        for match in self.compiled_patterns["ipc_section"].finditer(text):
            section_num = match.group(1)
            context = self._get_context(text, match.start(), match.end())
            
            citations.append(Citation(
                type=CitationType.IPC_SECTION,
                citation_text=f"Section {section_num} IPC",
                number=section_num,
                context=context
            ))
        
        return self._deduplicate_citations(citations)

    def _extract_cases(self, text: str) -> List[Citation]:
        """Extract case citations in various formats."""
        citations = []
        
        # SCC format: [2021] SCC 45
        for match in self.compiled_patterns["case_scc"].finditer(text):
            year = int(match.group(1))
            page = match.group(2)
            context = self._get_context(text, match.start(), match.end())
            
            citations.append(Citation(
                type=CitationType.CASE,
                citation_text=f"[{year}] SCC {page}",
                year=year,
                reporter="SCC",
                context=context
            ))
        
        # AIR format: AIR 2021 SC 123
        for match in self.compiled_patterns["case_air"].finditer(text):
            year = int(match.group(1))
            court = match.group(2)
            page = match.group(3)
            context = self._get_context(text, match.start(), match.end())
            
            citations.append(Citation(
                type=CitationType.CASE,
                citation_text=f"AIR {year} {court} {page}",
                year=year,
                reporter=f"AIR {court}",
                context=context
            ))
        
        return self._deduplicate_citations(citations)

    def _extract_acts(self, text: str) -> List[Citation]:
        """Extract acts and laws."""
        citations = []
        
        for match in self.compiled_patterns["acts"].finditer(text):
            act_name = match.group(1).strip()
            if len(act_name) > 3:  # Filter out short matches
                context = self._get_context(text, match.start(), match.end())
                
                citations.append(Citation(
                    type=CitationType.ACT,
                    citation_text=f"{act_name} Act",
                    context=context
                ))
        
        return self._deduplicate_citations(citations)

    def _extract_articles(self, text: str) -> List[Citation]:
        """Extract constitutional articles."""
        citations = []
        
        for match in self.compiled_patterns["article"].finditer(text):
            article_num = match.group(1)
            context = self._get_context(text, match.start(), match.end())
            
            citations.append(Citation(
                type=CitationType.ARTICLE,
                citation_text=f"Article {article_num}",
                number=article_num,
                context=context
            ))
        
        return self._deduplicate_citations(citations)

    def _extract_rules(self, text: str) -> List[Citation]:
        """Extract rule citations."""
        citations = []
        
        for match in self.compiled_patterns["rules"].finditer(text):
            rule_num = match.group(1)
            context = self._get_context(text, match.start(), match.end())
            
            citations.append(Citation(
                type=CitationType.RULE,
                citation_text=f"Rule {rule_num}",
                number=rule_num,
                context=context
            ))
        
        return self._deduplicate_citations(citations)

    def _extract_schedules(self, text: str) -> List[Citation]:
        """Extract schedule references."""
        citations = []
        
        for match in self.compiled_patterns["schedule"].finditer(text):
            schedule_num = match.group(1)
            context = self._get_context(text, match.start(), match.end())
            
            citations.append(Citation(
                type=CitationType.SCHEDULE,
                citation_text=f"Schedule {schedule_num}",
                number=schedule_num,
                context=context
            ))
        
        return citations

    def _extract_amendments(self, text: str) -> List[Citation]:
        """Extract amendment references."""
        citations = []
        
        for match in self.compiled_patterns["amendment"].finditer(text):
            amendment_num = match.group(1)
            context = self._get_context(text, match.start(), match.end())
            
            citations.append(Citation(
                type=CitationType.AMENDMENT,
                citation_text=f"{amendment_num} Amendment",
                number=amendment_num,
                context=context
            ))
        
        return citations

    @staticmethod
    def _get_context(text: str, start: int, end: int, context_length: int = 100) -> str:
        """Get surrounding context of citation."""
        context_start = max(0, start - context_length)
        context_end = min(len(text), end + context_length)
        
        context = text[context_start:context_end]
        
        # Clean up
        context = context.replace("\n", " ").strip()
        
        return f"...{context}..."

    @staticmethod
    def _deduplicate_citations(citations: List[Citation]) -> List[Citation]:
        """Remove duplicate citations while preserving order."""
        seen = set()
        unique = []
        
        for citation in citations:
            if citation.citation_text not in seen:
                seen.add(citation.citation_text)
                unique.append(citation)
        
        return unique


class CitationFormatter:
    """
    Formats citations for display and document creation.
    """

    # Citation format templates
    FORMATS = {
        "markdown": {
            "ipc": "**Section {number} IPC**",
            "case": "[{citation}]({url})",
            "article": "**Article {number}**",
            "act": "**{name} Act**"
        },
        "html": {
            "ipc": "<b>Section {number} IPC</b>",
            "case": '<a href="{url}">{citation}</a>',
            "article": "<b>Article {number}</b>",
            "act": "<b>{name} Act</b>"
        },
        "plain": {
            "ipc": "Section {number} IPC",
            "case": "{citation}",
            "article": "Article {number}",
            "act": "{name} Act"
        },
        "latex": {
            "ipc": "\\textbf{{Section {number} IPC}}",
            "case": "\\cite{{{citation}}}",
            "article": "\\textbf{{Article {number}}}",
            "act": "\\textbf{{{name} Act}}"
        }
    }

    @staticmethod
    def format_citation(citation: Citation, format_type: str = "plain") -> str:
        """
        Format a single citation.
        
        Args:
            citation: Citation object
            format_type: "markdown", "html", "plain", or "latex"
        
        Returns:
            Formatted citation string
        """
        if format_type not in CitationFormatter.FORMATS:
            format_type = "plain"
        
        formats = CitationFormatter.FORMATS[format_type]
        
        if citation.type == CitationType.IPC_SECTION:
            return formats["ipc"].format(number=citation.number)
        elif citation.type == CitationType.CASE:
            return formats["case"].format(citation=citation.citation_text, url="")
        elif citation.type == CitationType.ARTICLE:
            return formats["article"].format(number=citation.number)
        elif citation.type == CitationType.ACT:
            return formats["act"].format(name=citation.citation_text.replace(" Act", ""))
        else:
            return citation.citation_text

    @staticmethod
    def format_bibliography(citations: Dict[str, List[Citation]], format_type: str = "plain") -> str:
        """
        Format all citations as a bibliography.
        
        Args:
            citations: Dictionary of extracted citations
            format_type: Output format
        
        Returns:
            Formatted bibliography string
        """
        bibliography = []
        
        if citations.get("cases"):
            bibliography.append("**Cases Cited:**")
            for citation in citations["cases"]:
                bibliography.append(f"  • {CitationFormatter.format_citation(citation, format_type)}")
        
        if citations.get("ipc_sections"):
            bibliography.append("\n**IPC Sections Cited:**")
            for citation in citations["ipc_sections"]:
                bibliography.append(f"  • {CitationFormatter.format_citation(citation, format_type)}")
        
        if citations.get("acts"):
            bibliography.append("\n**Acts/Laws Cited:**")
            for citation in citations["acts"]:
                bibliography.append(f"  • {CitationFormatter.format_citation(citation, format_type)}")
        
        if citations.get("articles"):
            bibliography.append("\n**Constitutional Articles:**")
            for citation in citations["articles"]:
                bibliography.append(f"  • {CitationFormatter.format_citation(citation, format_type)}")
        
        return "\n".join(bibliography)

    @staticmethod
    def create_citation_list(citations_dict: Dict[str, List[Citation]]) -> List[Dict]:
        """
        Convert citations to list of dictionaries (for JSON export).
        """
        result = []
        
        for citation_type, citations_list in citations_dict.items():
            for citation in citations_list:
                result.append({
                    "type": citation.type.value,
                    "text": citation.citation_text,
                    "year": citation.year,
                    "number": citation.number,
                    "reporter": citation.reporter,
                    "context": citation.context
                })
        
        return result


class CitationLinker:
    """
    Links citations to actual case law or legal resources.
    """

    # Common Indian legal databases/URLs
    RESOURCES = {
        "indian_kanoon": "https://indiankanoon.org/",
        "scourt": "https://www.sci.gov.in/",
        "manupatra": "https://www.manupatra.com/",
        "legalbharti": "https://www.legalbharti.in/"
    }

    @staticmethod
    def link_case_citation(citation: Citation, database: str = "indian_kanoon") -> Optional[str]:
        """
        Generate a link to case law citation.
        
        Args:
            citation: Case citation
            database: Which database to link to
        
        Returns:
            URL to case law
        """
        if citation.type != CitationType.CASE:
            return None
        
        if database == "indian_kanoon":
            # Construct Indian Kanoon URL
            # e.g., https://indiankanoon.org/doc/[CASE_ID]/
            # Would need actual case ID mapping
            return f"{CitationLinker.RESOURCES['indian_kanoon']}search/?q={citation.citation_text}"
        
        return None

    @staticmethod
    def link_ipc_section(section_num: str, database: str = "indian_kanoon") -> str:
        """
        Generate a link to IPC section.
        
        Args:
            section_num: Section number
            database: Which database to link to
        
        Returns:
            URL to IPC section
        """
        if database == "indian_kanoon":
            # Common pattern for IPC sections on Indian Kanoon
            return f"{CitationLinker.RESOURCES['indian_kanoon']}search/?q=section+{section_num}+IPC"
        
        return ""


if __name__ == "__main__":
    # Demo
    print("\n" + "="*60)
    print("Citation Tracking Demo")
    print("="*60)
    
    sample_text = """
    The Supreme Court in [2021] SCC 45 held that Section 302 IPC prescribes life imprisonment.
    This principle was followed in AIR 2022 SC 123. According to Article 21 of the Constitution,
    no person shall be deprived of life or liberty except according to procedure established by law.
    The Criminal Procedure Code, 2023 Rule 5 also applies. This is the 73rd Amendment.
    """
    
    extractor = CitationExtractor()
    citations = extractor.extract_all(sample_text)
    
    print("\nExtracted Citations:")
    for citation_type, citation_list in citations.items():
        if citation_list:
            print(f"\n{citation_type.upper()}:")
            for citation in citation_list:
                print(f"  • {citation.citation_text}")
    
    # Format as bibliography
    formatter = CitationFormatter()
    bibliography = formatter.format_bibliography(citations)
    
    print("\n" + "="*60)
    print("Bibliography:")
    print("="*60)
    print(bibliography)
