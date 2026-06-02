"""
Quick Start Script: Complete Workflow from PDF to Vector Store
Run this to test the entire ingestion, chunking, embedding, and storage pipeline.
"""

import json
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_sample_documents():
    """Create sample legal documents for testing."""
    samples_dir = Path("data/raw_pdfs")
    samples_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample JSON documents (simulating extracted PDFs)
    sample_docs = [
        {
            "metadata": {
                "case_name": "State v. Sharma [2021]",
                "court_name": "Supreme Court",
                "judgment_date": "15th March 2021",
                "citation": "[2021] SCC 45",
                "judges": ["Justice Bench", "Justice Kumar"],
                "ipc_sections": ["Section 302", "Section 504"],
                "document_source": "judgment1.pdf",
                "file_name": "judgment1",
                "total_pages": 25,
                "extraction_date": "2024-01-01T00:00:00"
            },
            "full_text": """
            JUDGMENT
            
            In the matter of State v. Sharma [2021]
            
            Held by: The Hon'ble Supreme Court of India
            
            Judgment Date: 15th March 2021
            
            Citation: [2021] SCC 45
            
            The Supreme Court has held that Section 302 of the Indian Penal Code prescribes 
            life imprisonment as punishment for murder. The essential ingredients of murder are:
            
            1. Causing death by act
            2. Knowledge of the death-causing nature of act
            3. Intention to cause death or knowledge that act is death-causing
            
            Section 504 deals with intentional insult with intent to provoke breach of peace.
            
            The accused was convicted under Section 302 IPC and sentenced to life imprisonment.
            
            The judgment sets important precedents for understanding the distinction between
            murder and culpable homicide.
            """,
            "page_contents": [
                {
                    "page_num": 1,
                    "text": "SUPREME COURT OF INDIA\nJUDGMENT\nState v. Sharma [2021]\n[2021] SCC 45"
                }
            ]
        },
        {
            "metadata": {
                "case_name": "Bail Application - NDPS Case [2022]",
                "court_name": "High Court",
                "judgment_date": "20th June 2022",
                "citation": "AIR 2022 HC 321",
                "judges": ["Justice Patel"],
                "ipc_sections": ["Section 21", "Section 29"],
                "document_source": "judgment2.pdf",
                "file_name": "judgment2",
                "total_pages": 15,
                "extraction_date": "2024-01-01T00:00:00"
            },
            "full_text": """
            HIGH COURT JUDGMENT
            
            Bail Application in NDPS Case [2022]
            
            The High Court examined the bail provisions under the Narcotic Drugs and 
            Psychotropic Substances (NDPS) Act, 1985.
            
            Section 21 of NDPS Act deals with punishment for consumption of narcotic drugs.
            Section 29 provides enhanced punishment for subsequent offences.
            
            The Court held that:
            
            1. Bail in NDPS cases is discretionary, not absolute right
            2. The gravity of offence must be considered
            3. Likelihood of flight must be assessed
            4. Criminal antecedents are relevant
            
            Stringent conditions were imposed including:
            - Regular reporting to police station
            - Surrender of passport
            - Furnishing of surety bond
            
            The application was partly allowed with strict conditions.
            """,
            "page_contents": [
                {
                    "page_num": 1,
                    "text": "HIGH COURT OF [STATE]\nBAIL APPLICATION\nNDPS Case [2022]\nAIR 2022 HC 321"
                }
            ]
        }
    ]
    
    # Save samples
    for doc in sample_docs:
        file_path = samples_dir / f"{doc.get('metadata', {}).get('file_name', 'unknown')}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        logger.info(f"Created sample document: {file_path}")
    
    return samples_dir


def step1_extract_pdfs(pdf_dir, output_dir):
    """Step 1: Extract PDFs (simulated with sample JSON)."""
    logger.info("\n" + "="*60)
    logger.info("STEP 1: PDF Extraction")
    logger.info("="*60)
    
    from src.ingestion.pdf_loader import batch_load_pdfs
    
    # For demo, we'll load the sample JSON directly
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Loading documents from: {pdf_dir}")
    
    # Copy sample files to processed folder
    for json_file in Path(pdf_dir).glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        output_file = output_path / json_file.name
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✓ Extracted: {json_file.name}")
    
    return list(output_path.glob("*.json"))


def step2_chunk_documents(json_dir, output_dir):
    """Step 2: Chunk documents."""
    logger.info("\n" + "="*60)
    logger.info("STEP 2: Document Chunking")
    logger.info("="*60)
    
    from src.ingestion.chunker import LegalDocumentChunker
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    chunker = LegalDocumentChunker(
        chunk_size=500,
        chunk_overlap=100,
        preserve_sections=True
    )
    
    all_chunks = []
    
    for json_file in Path(json_dir).glob("*.json"):
        logger.info(f"Chunking: {json_file.name}")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            doc_data = json.load(f)
        
        metadata = doc_data.get('metadata', {})
        text = doc_data.get('full_text', '')
        page_contents = doc_data.get('page_contents', [])
        
        chunks = chunker.chunk_document(text, metadata, page_contents)
        logger.info(f"  Created {len(chunks)} chunks")
        
        # Save chunks
        output_file = output_path / f"{metadata.get('file_name', 'unknown')}_chunks.json"
        chunker.chunks_to_json(chunks, str(output_file))
        all_chunks.extend(chunks)
    
    logger.info(f"✓ Total chunks created: {len(all_chunks)}")
    return all_chunks


def step3_generate_embeddings(chunks_dir, output_dir):
    """Step 3: Generate embeddings."""
    logger.info("\n" + "="*60)
    logger.info("STEP 3: Generate Embeddings")
    logger.info("="*60)
    
    from src.ingestion.embedder import LegalEmbedder
    
    embedder = LegalEmbedder(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        batch_size=32
    )
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Embedder info: {embedder.get_model_info()}")
    
    embedded_files = []
    
    for json_file in Path(chunks_dir).glob("*_chunks.json"):
        logger.info(f"Embedding: {json_file.name}")
        
        output_file = output_path / f"{json_file.stem}_embedded.json"
        embedder.embed_json_file(str(json_file), str(output_file), use_cache=False)
        embedded_files.append(str(output_file))
        
        logger.info(f"  Saved to: {output_file.name}")
    
    logger.info(f"✓ Generated embeddings for {len(embedded_files)} files")
    return embedded_files


def step4_build_vector_store(embedded_dir):
    """Step 4: Build vector store with hybrid search."""
    logger.info("\n" + "="*60)
    logger.info("STEP 4: Build Vector Store & Hybrid Retriever")
    logger.info("="*60)
    
    from src.ingestion.embedder import LegalEmbedder
    from src.retrieval.vector_store import ChromaDBStore, load_and_index_chunks
    
    # Create embedder
    embedder = LegalEmbedder()
    
    # Create vector store
    vector_store = ChromaDBStore(
        persist_dir="./data/chromadb",
        collection_name="legal_documents"
    )
    
    logger.info("Loading chunks into vector store...")
    
    # Load and index
    retriever = load_and_index_chunks(
        embedded_dir,
        vector_store,
        embedder
    )
    
    # Get stats
    stats = vector_store.get_stats()
    logger.info(f"Vector Store Stats: {stats}")
    logger.info("✓ Vector store built successfully")
    
    return retriever, embedder, vector_store


def test_retrieval(retriever):
    """Test the retrieval system."""
    logger.info("\n" + "="*60)
    logger.info("STEP 5: Test Hybrid Retrieval")
    logger.info("="*60)
    
    # Test queries
    test_queries = [
        "What is the punishment for murder under Indian law?",
        "What are the bail provisions in NDPS cases?",
        "Section 302 IPC",
    ]
    
    for query in test_queries:
        logger.info(f"\nQuery: '{query}'")
        logger.info("-" * 60)
        
        results = retriever.hybrid_search(
            query=query,
            top_k=3,
            dense_weight=0.6,
            bm25_weight=0.4
        )
        
        if not results:
            logger.info("  No results found")
            continue
        
        for i, result in enumerate(results, 1):
            logger.info(f"\n  Result {i}:")
            logger.info(f"    Case: {result.case_name}")
            logger.info(f"    Court: {result.court_name}")
            logger.info(f"    Score: {result.similarity_score:.4f}")
            logger.info(f"    IPC: {', '.join(result.ipc_sections)}")
            logger.info(f"    Citations: {', '.join(result.case_citations)}")
            logger.info(f"    Pages: {result.page_numbers}")
            logger.info(f"    Method: {result.retrieval_method}")
            logger.info(f"    Text: {result.text[:100]}...")


def main():
    """Execute the complete workflow."""
    logger.info("\n" + "="*60)
    logger.info("INDIAN LEGAL ASSISTANT - COMPLETE WORKFLOW")
    logger.info("="*60)
    
    try:
        # Create sample documents
        logger.info("\nCreating sample documents for testing...")
        pdf_dir = create_sample_documents()
        
        # Step 1: Extract PDFs
        extracted_dir = "data/processed"
        step1_extract_pdfs(pdf_dir, extracted_dir)
        
        # Step 2: Chunk documents
        chunks_dir = "data/processed/chunks"
        step2_chunk_documents(extracted_dir, chunks_dir)
        
        # Step 3: Generate embeddings
        embedded_dir = "data/processed/chunks/embedded"
        step3_generate_embeddings(chunks_dir, embedded_dir)
        
        # Step 4: Build vector store
        retriever, embedder, vector_store = step4_build_vector_store(embedded_dir)
        
        # Step 5: Test retrieval
        test_retrieval(retriever)
        
        logger.info("\n" + "="*60)
        logger.info("✅ COMPLETE WORKFLOW EXECUTED SUCCESSFULLY!")
        logger.info("="*60)
        logger.info("\nNext Steps:")
        logger.info("1. Add your own legal PDF documents to data/raw_pdfs/")
        logger.info("2. Run this script again to process them")
        logger.info("3. Use retriever.hybrid_search() for custom queries")
        logger.info("\nVector store persisted at: ./data/chromadb")
        
    except Exception as e:
        logger.error(f"❌ Error during workflow: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
