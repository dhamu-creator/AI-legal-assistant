"""Ingestion pipeline for processing legal documents"""

try:
    from .pdf_loader import LegalPDFLoader, batch_load_pdfs, LegalDocumentMetadata, LegalDocument
except Exception:
    LegalPDFLoader = None
    batch_load_pdfs = None
    LegalDocumentMetadata = None
    LegalDocument = None

try:
    from .chunker import LegalDocumentChunker, chunk_legal_documents_batch, LegalChunk
except Exception:
    LegalDocumentChunker = None
    chunk_legal_documents_batch = None
    LegalChunk = None

try:
    from .embedder import LegalEmbedder, EmbeddingCache, compute_embedding_statistics
except Exception:
    LegalEmbedder = None
    EmbeddingCache = None
    compute_embedding_statistics = None

__all__ = [
    "LegalPDFLoader",
    "batch_load_pdfs",
    "LegalDocumentMetadata",
    "LegalDocument",
    "LegalDocumentChunker",
    "chunk_legal_documents_batch",
    "LegalChunk",
    "LegalEmbedder",
    "EmbeddingCache",
    "compute_embedding_statistics",
]
