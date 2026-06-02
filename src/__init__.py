"""
Indian Legal Assistant - RAG System
A full-stack AI-powered legal assistant for Indian courts using retrieval-augmented generation.
"""

__version__ = "0.1.0"
__author__ = "Legal AI Team"

try:
    from src.ingestion.pdf_loader import LegalPDFLoader, batch_load_pdfs
except Exception:
    LegalPDFLoader = None
    batch_load_pdfs = None

try:
    from src.ingestion.chunker import LegalDocumentChunker, chunk_legal_documents_batch
except Exception:
    LegalDocumentChunker = None
    chunk_legal_documents_batch = None

__all__ = [
    "LegalPDFLoader",
    "batch_load_pdfs",
    "LegalDocumentChunker",
    "chunk_legal_documents_batch",
]
