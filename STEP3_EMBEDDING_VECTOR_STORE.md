# STEP 3: Embedding & Vector Store - Complete Guide

## Overview

This step transforms extracted legal chunks into embeddings and stores them in a vector database with hybrid search capabilities (dense vectors + BM25 keyword search).

## Architecture

```
Legal Documents (PDF)
        ↓
   [STEP 1] PDF Extraction
        ↓
   Extracted Text + Metadata
        ↓
   [STEP 2] Smart Chunking
        ↓
   Document Chunks with IPC/Citations
        ↓
   [STEP 3] Embedding & Vector Store ← YOU ARE HERE
        ↓
   ┌─────────────────────────┐
   │  ChromaDB Vector Store  │
   │  ├─ Dense Embeddings    │
   │  ├─ BM25 Index          │
   │  └─ Metadata Filtering  │
   └─────────────────────────┘
        ↓
   Hybrid Retriever
        ↓
   [STEP 4] Retrieval (Dense + Keyword Search)
```

## Components

### 1. LegalEmbedder (embedder.py)

Generates embeddings for legal document chunks using sentence-transformers.

**Key Classes:**
- `LegalEmbedder` - Main embedder class
- `EmbeddingCache` - Caches embeddings for reuse

**Key Methods:**
- `embed_text(text)` - Embed a single text
- `embed_texts(texts)` - Embed multiple texts efficiently (batched)
- `embed_chunks(chunks)` - Embed list of chunk objects
- `embed_json_file(json_path)` - Load chunks from JSON, embed, save
- `batch_embed_directory()` - Process entire directory
- `similarity_search()` - Find similar docs to a query
- `get_model_info()` - Get model details

**Features:**
✅ Uses sentence-transformers/all-MiniLM-L6-v2 (384-dimensional embeddings)  
✅ GPU acceleration (CUDA if available, falls back to CPU)  
✅ Batch processing for efficiency (32 texts per batch)  
✅ Embedding normalization (unit vectors for cosine similarity)  
✅ Disk caching to avoid re-computing  
✅ Comprehensive statistics generation  

### 2. ChromaDBStore (vector_store.py)

Manages persistent storage in ChromaDB with metadata and filtering.

**Key Features:**
- ✅ Persistent local storage in DuckDB format
- ✅ Rich metadata support (case_name, court_type, IPC sections, citations)
- ✅ Supports metadata-based filtering
- ✅ Batch insertion for efficiency
- ✅ Multiple collection support

**Key Methods:**
- `add_chunk()` - Add single chunk
- `add_chunks_batch()` - Add multiple chunks at once
- `search_by_embedding()` - Dense vector search with optional filters
- `get_stats()` - Collection statistics
- `persist()` - Save to disk
- `reset()` - Clear collection

### 3. HybridRetriever (vector_store.py)

Combines dense vector search with BM25 keyword search using Reciprocal Rank Fusion (RRF).

**Key Methods:**
- `index_chunks()` - Build BM25 index from chunks
- `search_bm25()` - Keyword search
- `search_dense()` - Vector search
- `hybrid_search()` - Combined search with RRF fusion
- `filter_by_court()` - Court-based filtering
- `filter_by_ipc_section()` - IPC section filtering
- `filter_by_year_range()` - Year range filtering

**Hybrid Search Algorithm (RRF):**
```
For each search method (dense, BM25):
  1. Get top-k results with scores
  2. Weight results: dense_weight=0.6, bm25_weight=0.4
  3. Convert rank to RRF score: weight / (k_rrf + rank)
  4. Fuse scores for each document
  5. Sort by fused score
  6. Return top-k
```

## Complete Workflow

### Step-by-Step: From PDFs to Searchable Vector Store

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Extract and Chunk Documents (Previous Steps)

```python
from src.ingestion.pdf_loader import batch_load_pdfs
from src.ingestion.chunker import chunk_legal_documents_batch

# Extract PDFs
batch_load_pdfs(
    pdf_directory="data/raw_pdfs",
    output_directory="data/processed"
)

# Chunk documents
chunk_legal_documents_batch(
    json_directory="data/processed",
    output_directory="data/processed/chunks",
    chunk_size=500,
    chunk_overlap=100
)
```

#### 3. Generate Embeddings

**Option A: Embed Individual File**

```python
from src.ingestion.embedder import LegalEmbedder

embedder = LegalEmbedder(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    batch_size=32
)

# Embed a single chunked document
output_file = embedder.embed_json_file(
    json_path="data/processed/chunks/document1_chunks.json",
    output_path="data/processed/chunks/document1_chunks_embedded.json",
    use_cache=True
)

print(f"Embedded chunks saved to: {output_file}")
```

**Option B: Batch Embed Entire Directory**

```python
# Embed all chunk files
output_files = embedder.batch_embed_directory(
    input_dir="data/processed/chunks",
    output_dir="data/processed/chunks/embedded",
    pattern="*.json"
)

print(f"Embedded {len(output_files)} files")
```

#### 4. Load into Vector Store

```python
from src.retrieval.vector_store import ChromaDBStore, HybridRetriever, load_and_index_chunks

# Create vector store
vector_store = ChromaDBStore(
    persist_dir="./data/chromadb",
    collection_name="legal_documents"
)

# Create embedder for query encoding
embedder = LegalEmbedder()

# Load all embedded chunks and build indices
retriever = load_and_index_chunks(
    json_dir="data/processed/chunks/embedded",
    vector_store=vector_store,
    embedder=embedder
)

# Verify
stats = vector_store.get_stats()
print(f"Stored {stats['num_documents']} chunks in vector store")
```

#### 5. Perform Hybrid Search

```python
# Search
query = "What are the rights of an accused person arrested without warrant?"

results = retriever.hybrid_search(
    query=query,
    top_k=5,
    dense_weight=0.6,
    bm25_weight=0.4
)

# Display results
for i, result in enumerate(results, 1):
    print(f"\n{i}. {result.case_name} (Score: {result.similarity_score:.4f})")
    print(f"   Court: {result.court_name}")
    print(f"   IPC Sections: {', '.join(result.ipc_sections)}")
    print(f"   Citations: {', '.join(result.case_citations)}")
    print(f"   Text: {result.text[:150]}...")
    print(f"   Pages: {result.page_numbers}")
    print(f"   Method: {result.retrieval_method}")
```

#### 6. Filtered Search Examples

```python
# Filter by court type
where_filter = retriever.filter_by_court("Supreme Court")
results = retriever.hybrid_search(query, where_filter=where_filter)

# Filter by IPC section
where_filter = retriever.filter_by_ipc_section("Section 302")
results = retriever.hybrid_search(query, where_filter=where_filter)

# Custom metadata filter
where_filter = {
    "case_name": {"$contains": "State"}
}
results = retriever.hybrid_search(query, where_filter=where_filter)
```

## Configuration Options

Edit `.env` file:

```bash
# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# Vector Database
VECTOR_DB_TYPE=chromadb
CHROMADB_PATH=./data/chromadb

# Retrieval
TOP_K_CHUNKS=5
SIMILARITY_THRESHOLD=0.5

# Hybrid Search
DENSE_WEIGHT=0.6
BM25_WEIGHT=0.4
```

## Performance Considerations

### Embeddings
- **Model**: all-MiniLM-L6-v2 (384 dimensions)
  - Fast (~100 docs/second on CPU)
  - Good quality for legal domain
  - 123MB total size
- **Batch Size**: 32 (automatic batching for efficiency)
- **GPU**: Auto-detects CUDA, ~10x faster if available

### Vector Search
- **Index Type**: HNSW (Hierarchical Navigable Small World)
- **Distance Metric**: Cosine similarity
- **Indexing Time**: ~0.1ms per query (after warmup)

### BM25 Search
- **Time Complexity**: O(n*m) where n=docs, m=query tokens
- **Typical Time**: ~1-5ms for 10k documents
- **Good for**: Exact phrase matching, rare keywords

### Hybrid Search (RRF)
- **Combined Time**: Dense (~10ms) + BM25 (~3ms) ≈ **~15ms total**
- **Fusion**: Instant (simple arithmetic operations)

## Metadata Stored Per Chunk

```json
{
  "chunk_id": "document1_s2_c3",
  "text": "Section 302 of the Indian Penal Code...",
  "embedding": [0.123, -0.456, 0.789, ...],
  "case_name": "State v. Sharma [2022]",
  "court_name": "Supreme Court",
  "source_file": "document1",
  "chunk_type": "judgment",
  "page_numbers": [5, 6],
  "ipc_sections": ["Section 302", "Section 504"],
  "case_citations": ["[2022] SCC 45", "AIR 2021 SC 123"]
}
```

## Example: Complete Pipeline

```python
import json
from pathlib import Path
from src.ingestion.pdf_loader import LegalPDFLoader, batch_load_pdfs
from src.ingestion.chunker import LegalDocumentChunker, chunk_legal_documents_batch
from src.ingestion.embedder import LegalEmbedder
from src.retrieval.vector_store import ChromaDBStore, load_and_index_chunks

def build_legal_knowledge_base(pdf_folder, output_folder="./data"):
    """Build complete vector store from PDF folder."""
    
    print("Step 1: Extract PDFs")
    batch_load_pdfs(pdf_folder, f"{output_folder}/processed")
    
    print("Step 2: Chunk documents")
    chunk_legal_documents_batch(
        f"{output_folder}/processed",
        f"{output_folder}/processed/chunks",
        chunk_size=500,
        chunk_overlap=100
    )
    
    print("Step 3: Generate embeddings")
    embedder = LegalEmbedder()
    embedder.batch_embed_directory(
        f"{output_folder}/processed/chunks",
        f"{output_folder}/processed/chunks/embedded"
    )
    
    print("Step 4: Load into vector store")
    vector_store = ChromaDBStore(f"{output_folder}/chromadb")
    retriever = load_and_index_chunks(
        f"{output_folder}/processed/chunks/embedded",
        vector_store,
        embedder
    )
    
    print("✅ Knowledge base built successfully!")
    return retriever, embedder

# Usage
if __name__ == "__main__":
    retriever, embedder = build_legal_knowledge_base("data/raw_pdfs")
    
    # Test search
    query = "What are the rights during police interrogation?"
    results = retriever.hybrid_search(query, top_k=3)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.case_name}")
        print(f"   Similarity: {result.similarity_score:.4f}")
        print(f"   IPC: {result.ipc_sections}")
```

## Troubleshooting

### Issue: CUDA not detected
```python
# Force CPU
embedder = LegalEmbedder(device="cpu")

# Or force CUDA
embedder = LegalEmbedder(device="cuda")
```

### Issue: Out of memory
```python
# Reduce batch size
embedder = LegalEmbedder(batch_size=8)
```

### Issue: ChromaDB permission error
```bash
# Reset ChromaDB
rm -rf data/chromadb
# Recreate on next run
```

### Issue: Slow embedding
```python
# Check device
info = embedder.get_model_info()
print(f"Device: {info['device']}")

# Install CUDA if on GPU machine:
# https://pytorch.org/get-started/locally/
```

## Output Structure

After Step 3, you'll have:

```
data/
├── raw_pdfs/
│   ├── judgment1.pdf
│   └── judgment2.pdf
├── processed/
│   ├── judgment1.json
│   ├── judgment2.json
│   └── chunks/
│       ├── judgment1_chunks.json
│       ├── judgment2_chunks.json
│       └── embedded/
│           ├── judgment1_chunks_embedded.json
│           └── judgment2_chunks_embedded.json
└── chromadb/          ← Vector store (persistent)
    └── [ChromaDB index files]
```

## Next Steps

Ready for **STEP 4: Hybrid Retriever Optimization** which will cover:
- Fine-tuning RRF parameters
- Custom similarity thresholds
- Query expansion
- Result post-processing
- Performance optimization

Confirm to proceed! 🚀

---

## Quick Reference

| Task | Code |
|------|------|
| Initialize embedder | `embedder = LegalEmbedder()` |
| Embed single text | `embedding = embedder.embed_text("text")` |
| Embed batch | `embeddings = embedder.embed_texts(texts_list)` |
| Create vector store | `vs = ChromaDBStore("./data/chromadb")` |
| Add chunks | `vs.add_chunks_batch(chunks, embeddings)` |
| Dense search | `retriever.search_dense(query, top_k=5)` |
| BM25 search | `retriever.search_bm25(query, top_k=5)` |
| Hybrid search | `retriever.hybrid_search(query, top_k=5)` |
| Filter by court | `retriever.filter_by_court("Supreme Court")` |
| Get stats | `vector_store.get_stats()` |
