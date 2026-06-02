import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path.cwd()))

from src.ingestion.chunker import chunk_legal_documents_batch
from src.ingestion.embedder import LegalEmbedder

def run_ingestion():
    print("Starting manual ingestion...")
    
    # 1. Chunking
    print("Step 1: Chunking documents...")
    all_chunks = chunk_legal_documents_batch(
        json_directory="data/raw_pdfs",
        output_directory="data/processed/chunks",
        chunk_size=500,
        chunk_overlap=100
    )
    print(f"Chunks created for {len(all_chunks)} files.")
    
    # 2. Embedding
    print("Step 2: Generating embeddings...")
    embedder = LegalEmbedder()
    embedder.batch_embed_directory(
        input_dir="data/processed/chunks",
        output_dir="data/processed/chunks/embedded"
    )
    print("Embeddings generated.")

if __name__ == "__main__":
    run_ingestion()
