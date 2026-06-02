"""
Embedding Generator for Legal Documents
Generates embeddings using sentence-transformers and stores them with metadata.
"""

import json
import numpy as np
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import logging
from dataclasses import asdict

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SentenceTransformer = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    torch = None
    TORCH_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LegalEmbedder:
    """
    Generates embeddings for legal document chunks using sentence-transformers.
    Supports batching for efficient processing and GPU acceleration.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: Optional[str] = None,
        batch_size: int = 32,
        cache_folder: str = "./cache/embeddings"
    ):
        """
        Initialize the embedder.
        
        Args:
            model_name: HuggingFace model ID for sentence-transformers
            device: Device to use ('cuda', 'cpu', or None for auto-detect)
            batch_size: Number of texts to embed at once
            cache_folder: Where to cache embeddings
        """
        self.model_name = model_name
        self.batch_size = batch_size
        self.cache_folder = Path(cache_folder)
        self.cache_folder.mkdir(parents=True, exist_ok=True)

        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "sentence-transformers is not installed. "
                "Run: pip install sentence-transformers"
            )

        # Auto-detect device
        if device is None:
            self.device = "cuda" if (TORCH_AVAILABLE and torch.cuda.is_available()) else "cpu"
        else:
            self.device = device

        logger.info(f"Loading model: {model_name}")
        logger.info(f"Using device: {self.device}")

        # Load model with local_files_only to avoid rate limiting
        try:
            self.model = SentenceTransformer(
                model_name,
                device=self.device,
                cache_folder=str(self.cache_folder),
                local_files_only=True  # Force use of cached files only
            )
            logger.info("Model loaded from local cache")
        except Exception as e:
            logger.warning(f"Local cache failed: {e}. Downloading model...")
            try:
                self.model = SentenceTransformer(
                    model_name,
                    device=self.device,
                    cache_folder=str(self.cache_folder)
                )
                logger.info("Model downloaded successfully")
            except Exception as e2:
                logger.error(f"Failed to load model: {e2}")
                raise RuntimeError(f"Cannot load embedding model. Error: {str(e2)}")

        self.embedding_dim = self.model.get_sentence_embedding_dimension()

        logger.info(f"Model loaded. Embedding dimension: {self.embedding_dim}")


    def embed_text(self, text: str, normalize: bool = True) -> np.ndarray:
        """
        Embed a single text string.
        
        Args:
            text: Text to embed
            normalize: Whether to normalize the embedding to unit vector
        
        Returns:
            Embedding as numpy array
        """
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=normalize
        )
        return embedding

    def embed_texts(
        self,
        texts: List[str],
        normalize: bool = True,
        show_progress: bool = True
    ) -> np.ndarray:
        """
        Embed multiple texts efficiently in batches.
        
        Args:
            texts: List of texts to embed
            normalize: Whether to normalize embeddings
            show_progress: Show progress bar
        
        Returns:
            2D numpy array of embeddings (n_texts, embedding_dim)
        """
        logger.info(f"Embedding {len(texts)} texts with batch size {self.batch_size}")

        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            convert_to_numpy=True,
            normalize_embeddings=normalize,
            show_progress_bar=show_progress
        )

        logger.info(f"Generated embeddings with shape: {embeddings.shape}")
        return embeddings

    def embed_chunks(
        self,
        chunks: List[Dict],
        use_cache: bool = True
    ) -> List[Dict]:
        """
        Embed a list of chunk dictionaries (as from chunker.py).
        
        Args:
            chunks: List of chunk dicts with 'chunk_id' and 'text' keys
            use_cache: Cache embeddings to disk
        
        Returns:
            List of chunks enriched with 'embedding' key
        """
        chunk_texts = [chunk.get("text", "") for chunk in chunks]
        
        logger.info(f"Embedding {len(chunks)} chunks")
        embeddings = self.embed_texts(chunk_texts, show_progress=True)

        # Attach embeddings to chunks
        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding.tolist()

        # Cache to disk if requested
        if use_cache:
            cache_file = self.cache_folder / f"embeddings_{len(chunks)}.npy"
            np.save(cache_file, embeddings)
            logger.info(f"Cached embeddings to {cache_file}")

        return chunks

    def embed_json_file(
        self,
        json_path: str,
        output_path: Optional[str] = None,
        use_cache: bool = True
    ) -> str:
        """
        Load chunks from JSON, embed them, and save to new JSON.
        
        Args:
            json_path: Path to input JSON with chunks
            output_path: Where to save output (auto-generated if None)
            use_cache: Cache embeddings
        
        Returns:
            Path to output JSON file
        """
        # Load chunks
        with open(json_path, 'r', encoding='utf-8') as f:
            chunks_data = json.load(f)

        # Handle both single chunk and list of chunks
        if isinstance(chunks_data, dict) and "text" in chunks_data:
            chunks_data = [chunks_data]

        # Embed chunks
        embedded_chunks = self.embed_chunks(chunks_data, use_cache=use_cache)

        # Save output
        if output_path is None:
            input_path = Path(json_path)
            output_path = str(input_path.parent / f"{input_path.stem}_embedded.json")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(embedded_chunks, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved embedded chunks to {output_path}")
        return output_path

    def batch_embed_directory(
        self,
        input_dir: str,
        output_dir: str,
        pattern: str = "*.json",
        use_cache: bool = True
    ) -> List[str]:
        """
        Batch embed all JSON files in a directory.
        
        Args:
            input_dir: Directory containing JSON files
            output_dir: Where to save embedded JSON files
            pattern: Glob pattern for files to process
            use_cache: Cache embeddings
        
        Returns:
            List of output file paths
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        output_files = []

        for json_file in sorted(input_path.glob(pattern)):
            try:
                output_file = output_path / f"{json_file.stem}_embedded.json"
                self.embed_json_file(str(json_file), str(output_file), use_cache)
                output_files.append(str(output_file))
            except Exception as e:
                logger.error(f"Failed to embed {json_file.name}: {str(e)}")

        logger.info(f"Batch embedding complete. Processed {len(output_files)} files.")
        return output_files

    def similarity_search(
        self,
        query: str,
        embeddings: np.ndarray,
        top_k: int = 5,
        threshold: float = 0.0
    ) -> List[Tuple[int, float]]:
        """
        Search embeddings for similar documents to a query.
        
        Args:
            query: Query text
            embeddings: 2D array of document embeddings (n_docs, embedding_dim)
            top_k: Number of top results to return
            threshold: Minimum similarity score
        
        Returns:
            List of (doc_index, similarity_score) tuples, sorted by similarity
        """
        # Embed query
        query_embedding = self.embed_text(query, normalize=True)

        # Compute cosine similarity (normalized embeddings)
        similarities = embeddings @ query_embedding

        # Filter by threshold
        valid_indices = np.where(similarities >= threshold)[0]
        valid_similarities = similarities[valid_indices]

        # Get top-k
        top_indices = np.argsort(-valid_similarities)[:top_k]
        results = [
            (valid_indices[idx].item(), valid_similarities[idx].item())
            for idx in top_indices
        ]

        return results

    def get_model_info(self) -> Dict:
        """Get information about the loaded model."""
        return {
            "model_name": self.model_name,
            "embedding_dim": self.embedding_dim,
            "device": self.device,
            "batch_size": self.batch_size
        }


class EmbeddingCache:
    """
    Manages caching of embeddings to improve performance on repeated queries.
    """

    def __init__(self, cache_dir: str = "./cache/embedding_cache"):
        """
        Initialize cache.
        
        Args:
            cache_dir: Directory to store embeddings cache
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache = {}

    def get_cache_file(self, key: str) -> Path:
        """Get cache file path for a key."""
        return self.cache_dir / f"{key}.npy"

    def save_embedding(self, key: str, embedding: np.ndarray) -> None:
        """Save embedding to cache."""
        np.save(self.get_cache_file(key), embedding)
        self.cache[key] = embedding

    def load_embedding(self, key: str) -> Optional[np.ndarray]:
        """Load embedding from cache."""
        cache_file = self.get_cache_file(key)
        if cache_file.exists():
            self.cache[key] = np.load(cache_file)
            return self.cache[key]
        return None

    def has_cached(self, key: str) -> bool:
        """Check if embedding is cached."""
        return self.get_cache_file(key).exists()

    def clear_cache(self) -> None:
        """Clear entire cache."""
        import shutil
        shutil.rmtree(self.cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache.clear()


def compute_embedding_statistics(embeddings: np.ndarray) -> Dict:
    """
    Compute statistics about embeddings for quality checks.
    
    Args:
        embeddings: 2D array of embeddings
    
    Returns:
        Dictionary with statistics
    """
    return {
        "num_embeddings": embeddings.shape[0],
        "embedding_dim": embeddings.shape[1],
        "mean_norm": float(np.mean(np.linalg.norm(embeddings, axis=1))),
        "std_norm": float(np.std(np.linalg.norm(embeddings, axis=1))),
        "min_norm": float(np.min(np.linalg.norm(embeddings, axis=1))),
        "max_norm": float(np.max(np.linalg.norm(embeddings, axis=1))),
        "mean_values": np.mean(embeddings, axis=0).tolist()[:5],  # First 5 dims
    }


if __name__ == "__main__":
    # Example usage
    embedder = LegalEmbedder(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("\n" + "="*50)
    print("Model Info:")
    info = embedder.get_model_info()
    for key, value in info.items():
        print(f"  {key}: {value}")

    # Test embedding a legal query
    queries = [
        "What are the rights of an accused person without a warrant?",
        "IPC section for cheating and fraud",
        "Bail provisions in NDPS cases"
    ]

    print("\n" + "="*50)
    print("Test Embeddings:")
    for query in queries:
        embedding = embedder.embed_text(query)
        print(f"Query: {query}")
        print(f"  Embedding shape: {embedding.shape}")
        print(f"  First 5 values: {embedding[:5]}")
        print()

    # Test batch embedding
    print("\n" + "="*50)
    print("Batch Embedding Test:")
    test_texts = [
        "Section 302 of IPC prescribes life imprisonment for murder",
        "The Supreme Court has ruled on bail conditions",
        "Domestic violence under PWDVA has specific remedies"
    ]
    batch_embeddings = embedder.embed_texts(test_texts)
    stats = compute_embedding_statistics(batch_embeddings)
    print(f"Statistics: {stats}")
