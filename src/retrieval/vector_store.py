"""
Vector Store for Legal Document Chunks
Manages ChromaDB/Weaviate storage with hybrid search (dense + BM25 keyword search).
"""

try:
    import pysqlite3
    import sys
    sys.modules["sqlite3"] = pysqlite3
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Using pysqlite3 as a fallback for sqlite3")
except ImportError:
    pass

import json
import logging
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    chromadb = None
    Settings = None
    CHROMADB_AVAILABLE = False

import numpy as np

try:
    from rank_bm25 import BM25Okapi
    BM25_AVAILABLE = True
except ImportError:
    BM25Okapi = None
    BM25_AVAILABLE = False

try:
    import nltk
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    nltk = None
    word_tokenize = None
    NLTK_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download NLTK tokenizer data only if NLTK is available
if NLTK_AVAILABLE and nltk is not None:
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        try:
            nltk.download('punkt_tab', quiet=True)
        except Exception:
            try:
                nltk.download('punkt', quiet=True)
            except Exception:
                pass


@dataclass
class RetrievalResult:
    """Result from vector search"""
    chunk_id: str
    text: str
    similarity_score: float
    ipc_sections: List[str]
    case_citations: List[str]
    case_name: str
    court_name: str
    page_numbers: List[int]
    retrieval_method: str  # "dense", "bm25", or "hybrid"


class ChromaDBStore:
    """
    Vector store using ChromaDB for efficient local storage and retrieval.
    Supports metadata filtering and hybrid search.
    """

    def __init__(
        self,
        persist_dir: str = "./data/chromadb",
        collection_name: str = "legal_documents",
        embedding_model: str = "default"
    ):
        """
        Initialize ChromaDB store.
        
        Args:
            persist_dir: Directory for persistent storage
            collection_name: Name of the collection
            embedding_model: Embedding model to use
        """
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.collection_name = collection_name

        if not CHROMADB_AVAILABLE:
            raise ImportError(
                "chromadb is not installed. Run: pip install chromadb"
            )

        # Initialize ChromaDB client with persistence (new API)
        try:
            # Try new PersistentClient API
            self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        except (AttributeError, TypeError):
            # Fallback to old API if new one doesn't work
            try:
                settings = Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=str(self.persist_dir),
                    anonymized_telemetry=False,
                    allow_reset=True
                )
                self.client = chromadb.Client(settings)
            except Exception as e:
                logger.warning(f"ChromaDB initialization issue: {e}. Using ephemeral client.")
                self.client = chromadb.EphemeralClient()
        
        logger.info(f"ChromaDB initialized at {self.persist_dir}")

        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            logger.info(f"Loaded existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Created new collection: {collection_name}")

    def add_chunk(
        self,
        chunk_id: str,
        text: str,
        embedding: List[float],
        metadata: Dict
    ) -> None:
        """
        Add a single chunk to the store.
        
        Args:
            chunk_id: Unique chunk identifier
            text: Chunk text
            embedding: Embedding vector
            metadata: Metadata dictionary
        """
        # Clean metadata for ChromaDB (only string/int/float values)
        clean_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)):
                clean_metadata[key] = value
            elif isinstance(value, list):
                # Convert lists to comma-separated strings
                clean_metadata[key] = ",".join(str(v) for v in value)
            else:
                clean_metadata[key] = str(value)

        self.collection.add(
            ids=[chunk_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[clean_metadata]
        )

    def add_chunks_batch(
        self,
        chunks: List[Dict],
        embeddings: np.ndarray
    ) -> None:
        """
        Add multiple chunks efficiently.
        
        Args:
            chunks: List of chunk dictionaries
            embeddings: 2D array of embeddings
        """
        chunk_ids = []
        texts = []
        embeddings_list = []
        metadatas = []

        for chunk, embedding in zip(chunks, embeddings):
            chunk_ids.append(chunk.get("chunk_id", "unknown"))
            texts.append(chunk.get("text", ""))
            embeddings_list.append(embedding.tolist())

            # Prepare metadata
            metadata = {
                "case_name": chunk.get("case_name", ""),
                "court_name": chunk.get("court_name", ""),
                "source_file": chunk.get("source_file", ""),
                "chunk_type": chunk.get("chunk_type", "body"),
                "page_numbers": ",".join(str(p) for p in chunk.get("page_numbers", [])),
                "ipc_sections": ",".join(chunk.get("ipc_sections", [])),
                "case_citations": ",".join(chunk.get("case_citations", []))
            }
            metadatas.append(metadata)

        self.collection.add(
            ids=chunk_ids,
            embeddings=embeddings_list,
            documents=texts,
            metadatas=metadatas
        )

        logger.info(f"Added {len(chunks)} chunks to ChromaDB")

    def search_by_embedding(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where_filter: Optional[Dict] = None
    ) -> List[RetrievalResult]:
        """
        Search by embedding vector.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            where_filter: ChromaDB where clause for filtering
        
        Returns:
            List of RetrievalResult objects
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where_filter
            )

            retrieval_results = []

            if results and results["ids"] and len(results["ids"]) > 0:
                for i, chunk_id in enumerate(results["ids"][0]):
                    # Extract metadata
                    metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                    
                    result = RetrievalResult(
                        chunk_id=chunk_id,
                        text=results["documents"][0][i] if results["documents"] else "",
                        similarity_score=1 - (results["distances"][0][i] if results["distances"] else 0),
                        ipc_sections=metadata.get("ipc_sections", "").split(",") if metadata.get("ipc_sections") else [],
                        case_citations=metadata.get("case_citations", "").split(",") if metadata.get("case_citations") else [],
                        case_name=metadata.get("case_name", ""),
                        court_name=metadata.get("court_name", ""),
                        page_numbers=[int(p) for p in metadata.get("page_numbers", "").split(",") if p],
                        retrieval_method="dense"
                    )
                    retrieval_results.append(result)

            return retrieval_results

        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []

    def get_stats(self) -> Dict:
        """Get statistics about the collection."""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "num_documents": count,
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
            }
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            return {}

    def persist(self) -> None:
        """Persist data to disk (no-op for PersistentClient which auto-persists)."""
        # PersistentClient (chromadb >= 0.4) persists automatically.
        # Old duckdb+parquet client required an explicit persist() call.
        if hasattr(self.client, 'persist'):
            try:
                self.client.persist()
                logger.info("ChromaDB persisted to disk")
            except Exception as e:
                logger.warning(f"ChromaDB persist() not supported on this client version: {e}")
        else:
            logger.info("ChromaDB PersistentClient: data is persisted automatically")

    def reset(self) -> None:
        """Reset the collection."""
        self.client.reset()
        logger.info("ChromaDB collection reset")


class HybridRetriever:
    """
    Hybrid retriever combining dense vector search with BM25 keyword search.
    Uses Reciprocal Rank Fusion (RRF) to merge results.
    """

    def __init__(
        self,
        vector_store: ChromaDBStore,
        embedder=None,
        k1: float = 1.5,
        b: float = 0.75,
        rrf_k: int = 60
    ):
        """
        Initialize hybrid retriever.
        
        Args:
            vector_store: ChromaDBStore instance
            embedder: LegalEmbedder instance for query embedding
            k1, b: BM25 parameters
            rrf_k: RRF parameter for rank fusion
        """
        self.vector_store = vector_store
        self.embedder = embedder
        self.rrf_k = rrf_k

        # Build BM25 index from existing documents
        self.documents_dict = {}  # chunk_id -> full chunk info
        self.bm25 = None
        self.corpus = []
        self.corpus_ids = []

        logger.info("Hybrid retriever initialized")

    def index_chunks(self, chunks: List[Dict]) -> None:
        """
        Build BM25 index from chunks.
        
        Args:
            chunks: List of chunk dictionaries
        """
        self.corpus = []
        self.corpus_ids = []
        self.documents_dict = {}

        for chunk in chunks:
            chunk_id = chunk.get("chunk_id", "")
            text = chunk.get("text", "")

            # Tokenize for BM25 (fall back to simple split if NLTK unavailable)
            if NLTK_AVAILABLE and word_tokenize is not None:
                tokens = word_tokenize(text.lower())
            else:
                tokens = text.lower().split()
            self.corpus.append(tokens)
            self.corpus_ids.append(chunk_id)
            self.documents_dict[chunk_id] = chunk

        # Build BM25
        if self.corpus:
            if BM25_AVAILABLE and BM25Okapi is not None:
                self.bm25 = BM25Okapi(self.corpus)
                logger.info(f"Built BM25 index for {len(self.corpus)} documents")
            else:
                logger.warning("rank-bm25 not installed; BM25 search disabled.")
                self.bm25 = None
        else:
            logger.warning("No documents to index for BM25.")
            self.bm25 = None

    def search_bm25(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Search using BM25 keyword search.
        
        Args:
            query: Query string
            top_k: Number of results
        
        Returns:
            List of (chunk_id, score) tuples
        """
        if not self.bm25:
            logger.warning("BM25 index not built. Run index_chunks() first.")
            return []

        if NLTK_AVAILABLE and word_tokenize is not None:
            query_tokens = word_tokenize(query.lower())
        else:
            query_tokens = query.lower().split()
        scores = self.bm25.get_scores(query_tokens)

        # Get top-k
        top_indices = np.argsort(-scores)[:top_k]
        results = [
            (self.corpus_ids[idx], float(scores[idx]))
            for idx in top_indices
            if scores[idx] > 0
        ]

        return results

    def search_dense(
        self,
        query: str,
        top_k: int = 5,
        where_filter: Optional[Dict] = None
    ) -> List[Tuple[str, float]]:
        """
        Search using dense embeddings.
        
        Args:
            query: Query string
            top_k: Number of results
            where_filter: Metadata filter
        
        Returns:
            List of (chunk_id, score) tuples
        """
        if not self.embedder:
            logger.warning("Embedder not available. Using BM25 only.")
            return []

        query_embedding = self.embedder.embed_text(query, normalize=True)
        results_obj = self.vector_store.search_by_embedding(
            query_embedding.tolist(),
            top_k=top_k,
            where_filter=where_filter
        )

        return [(r.chunk_id, r.similarity_score) for r in results_obj]

    def hybrid_search(
        self,
        query: str,
        top_k: int = 5,
        dense_weight: float = 0.6,
        bm25_weight: float = 0.4,
        where_filter: Optional[Dict] = None
    ) -> List[RetrievalResult]:
        """
        Hybrid search combining dense and BM25 with Reciprocal Rank Fusion.
        
        Args:
            query: Query string
            top_k: Number of final results
            dense_weight: Weight for dense search results
            bm25_weight: Weight for BM25 results
            where_filter: Metadata filter for dense search
        
        Returns:
            List of RetrievalResult objects
        """
        # Get results from both methods
        dense_results = self.search_dense(query, top_k=top_k*2, where_filter=where_filter)
        bm25_results = self.search_bm25(query, top_k=top_k*2)

        # Apply Reciprocal Rank Fusion
        scores = {}

        # Add dense results
        for rank, (chunk_id, score) in enumerate(dense_results, 1):
            rrf_score = dense_weight / (self.rrf_k + rank)
            scores[chunk_id] = scores.get(chunk_id, 0) + rrf_score

        # Add BM25 results
        for rank, (chunk_id, score) in enumerate(bm25_results, 1):
            rrf_score = bm25_weight / (self.rrf_k + rank)
            scores[chunk_id] = scores.get(chunk_id, 0) + rrf_score

        # Sort and get top-k
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        # Build full results
        retrieval_results = []
        for chunk_id, fused_score in sorted_results:
            chunk_info = self.documents_dict.get(chunk_id, {})

            result = RetrievalResult(
                chunk_id=chunk_id,
                text=chunk_info.get("text", ""),
                similarity_score=fused_score,
                ipc_sections=chunk_info.get("ipc_sections", []),
                case_citations=chunk_info.get("case_citations", []),
                case_name=chunk_info.get("case_name", ""),
                court_name=chunk_info.get("court_name", ""),
                page_numbers=chunk_info.get("page_numbers", []),
                retrieval_method="hybrid"
            )
            retrieval_results.append(result)

        logger.info(f"Hybrid search returned {len(retrieval_results)} results")
        return retrieval_results

    def filter_by_court(self, court_name: str) -> Dict:
        """Create a where filter for court type."""
        return {"court_name": {"$eq": court_name}}

    def filter_by_ipc_section(self, section_num: str) -> Dict:
        """Create a where filter for IPC section."""
        return {"ipc_sections": {"$contains": section_num}}

    def filter_by_year_range(
        self,
        citation: str,
        start_year: int,
        end_year: int
    ) -> Dict:
        """Create a where filter for year range (from citation)."""
        # Simple filter by citation pattern
        return {
            "case_citations": {
                "$contains": f"[{start_year}]"
            }
        }


def load_and_index_chunks(
    json_dir: str,
    vector_store: ChromaDBStore,
    embedder=None
) -> HybridRetriever:
    """
    Load chunks from JSON files and build vector store + BM25 index.
    
    Args:
        json_dir: Directory containing chunk JSON files
        vector_store: ChromaDBStore instance
        embedder: LegalEmbedder instance
    
    Returns:
        HybridRetriever instance ready for search
    """
    json_path = Path(json_dir)
    all_chunks = []

    # Load all chunks - priority to _embedded.json, fallback to _chunks.json
    patterns = ["*_embedded.json", "*_chunks.json"]
    loaded_files = set()

    for pattern in patterns:
        for json_file in sorted(json_path.glob(pattern)):
            # Avoid loading both embedded and raw for same file
            file_base = json_file.name.replace("_embedded.json", "").replace("_chunks.json", "")
            if file_base in loaded_files:
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                    if not isinstance(chunks, list):
                        chunks = [chunks]
                    if chunks:
                        all_chunks.extend(chunks)
                        loaded_files.add(file_base)
                        logger.info(f"Loaded {len(chunks)} chunks from {json_file.name}")
            except Exception as e:
                logger.error(f"Failed to load {json_file.name}: {str(e)}")

    logger.info(f"Loaded {len(all_chunks)} chunks total from {len(loaded_files)} files")

    # Extract embeddings and add to vector store
    embeddings = []
    chunks_with_embeddings = []
    for chunk in all_chunks:
        if "embedding" in chunk and chunk["embedding"]:
            embeddings.append(chunk["embedding"])
            chunks_with_embeddings.append(chunk)

    if chunks_with_embeddings:
        logger.info(f"Adding {len(chunks_with_embeddings)} chunks with embeddings to vector store")
        embeddings_array = np.array(embeddings)
        vector_store.add_chunks_batch(chunks_with_embeddings, embeddings_array)
    else:
        logger.warning("No embeddings found in any chunks. Vector search will be unavailable.")

    # Create hybrid retriever
    retriever = HybridRetriever(
        vector_store=vector_store,
        embedder=embedder
    )

    # Index chunks for BM25
    if all_chunks:
        retriever.index_chunks(all_chunks)
        logger.info(f"Indexed {len(all_chunks)} chunks for BM25 search")

    logger.info("Vector store and BM25 index ready")
    return retriever


if __name__ == "__main__":
    # Example usage
    from src.ingestion.embedder import LegalEmbedder

    print("\n" + "="*50)
    print("Initializing Vector Store and Embedder")

    # Create embedder
    embedder = LegalEmbedder()

    # Create vector store
    vector_store = ChromaDBStore(
        persist_dir="./data/chromadb",
        collection_name="legal_documents"
    )

    print("\nVector Store Stats:")
    stats = vector_store.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Create hybrid retriever
    retriever = HybridRetriever(
        vector_store=vector_store,
        embedder=embedder
    )

    # Test with sample chunks
    test_chunks = [
        {
            "chunk_id": "test_1",
            "text": "Section 302 IPC provides life imprisonment for murder",
            "case_name": "Test Case 1",
            "court_name": "Supreme Court",
            "ipc_sections": ["Section 302"],
            "case_citations": ["[2020] SCC 45"],
            "page_numbers": [1],
            "chunk_type": "body",
            "embedding": embedder.embed_text("Section 302 IPC provides life imprisonment for murder").tolist()
        },
        {
            "chunk_id": "test_2",
            "text": "Bail provisions in NDPS cases are strictly defined by Supreme Court precedents",
            "case_name": "Test Case 2",
            "court_name": "High Court",
            "ipc_sections": [],
            "case_citations": ["[2021] AIR 123"],
            "page_numbers": [2],
            "chunk_type": "judgment",
            "embedding": embedder.embed_text("Bail provisions in NDPS cases are strictly defined").tolist()
        }
    ]

    # Add to vector store
    embeddings = np.array([chunk["embedding"] for chunk in test_chunks])
    vector_store.add_chunks_batch(test_chunks, embeddings)

    # Index for BM25
    retriever.index_chunks(test_chunks)

    # Test search
    print("\n" + "="*50)
    print("Testing Hybrid Search:")
    query = "What is the punishment for murder in Indian law?"
    results = retriever.hybrid_search(query, top_k=2)

    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"  Case: {result.case_name}")
        print(f"  Score: {result.similarity_score:.4f}")
        print(f"  Text: {result.text[:100]}...")
        print(f"  IPC: {result.ipc_sections}")
