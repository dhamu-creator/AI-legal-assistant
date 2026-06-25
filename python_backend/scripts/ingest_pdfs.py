import os
os.environ['USE_TF'] = '0'
os.environ['USE_TORCH'] = '1'
import glob
import logging
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_DIR = os.path.join(DATA_DIR, "chroma_db")
OLD_DB_DIR = os.path.join(DATA_DIR, "simple_db")

def ingest_all_pdfs():
    """Reads all PDFs in DATA_DIR, chunks them, and stores embeddings locally using ChromaDB."""
    if not os.path.exists(DATA_DIR):
        logger.error(f"Data directory not found: {DATA_DIR}")
        return

    # Determine which directory has PDFs
    pdf_dir = DATA_DIR
    pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
    if not pdf_files:
        alt_pdf_dir = os.path.join(DATA_DIR, "pdfs")
        if os.path.exists(alt_pdf_dir):
            pdf_files = glob.glob(os.path.join(alt_pdf_dir, "*.pdf"))
            if pdf_files:
                pdf_dir = alt_pdf_dir
                
    if not pdf_files:
        logger.warning(f"No PDFs found in {DATA_DIR} or {os.path.join(DATA_DIR, 'pdfs')}")
        return

    logger.info(f"Found {len(pdf_files)} PDFs in {pdf_dir}. Loading via LangChain PyPDFLoader...")
    
    documents = []
    for pdf_file in pdf_files:
        logger.info(f"Loading {os.path.basename(pdf_file)}...")
        try:
            loader = PyPDFLoader(pdf_file)
            documents.extend(loader.load())
        except Exception as e:
            logger.error(f"Failed to load {pdf_file}: {e}")

    logger.info(f"Loaded {len(documents)} document pieces (pages).")
    
    if not documents:
        logger.warning("No text extracted from PDFs.")
        return
        
    logger.info("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Created {len(chunks)} text chunks.")

    # Clean old Chroma DB if it exists to avoid stale data
    if os.path.exists(DB_DIR):
        logger.info(f"Cleaning existing ChromaDB directory at {DB_DIR}...")
        shutil.rmtree(DB_DIR)

    os.makedirs(DB_DIR, exist_ok=True)
    
    # Configure global settings
    logger.info("Setting up HuggingFace embedding model (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    logger.info("Generating embeddings and building Chroma VectorStore. This may take a moment...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    
    logger.info(f"Persisted vector database to {DB_DIR}")

    # Remove the old LlamaIndex simple_db if we upgraded
    if os.path.exists(OLD_DB_DIR):
        try:
            logger.info("Removing deprecated LlamaIndex db...")
            shutil.rmtree(OLD_DB_DIR)
        except Exception as e:
            logger.warning(f"Failed to remove old LlamaIndex db: {e}")

    logger.info("Ingestion complete. The database is ready for RAG.")

if __name__ == "__main__":
    ingest_all_pdfs()
