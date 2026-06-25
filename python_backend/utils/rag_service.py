import os
os.environ['USE_TF'] = '0'
os.environ['USE_TORCH'] = '1'
import logging
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger("ai_legal_assistant")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "data", "chroma_db")

class RAGService:
    def __init__(self):
        self.vectorstore = None
        self._init_db()
        
    def _init_db(self):
        """Initialize the local Chroma vector database."""
        if not os.path.exists(DB_DIR) or not os.listdir(DB_DIR):
            logger.warning(f"Vector DB not found at {DB_DIR}. Make sure to run ingest_pdfs.py first.")
            return
            
        try:
            logger.info("Loading offline embedding model (all-MiniLM-L6-v2) for LangChain...")
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
            # Load the Chroma DB from the persisted directory
            logger.info(f"Loading index from storage at {DB_DIR}...")
            self.vectorstore = Chroma(
                persist_directory=DB_DIR, 
                embedding_function=embeddings
            )
            logger.info("Successfully loaded ChromaDB RAG.")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            self.vectorstore = None

    def search(self, query: str, n_results: int = 4) -> list:
        """
        Search the vector database for text relevant to the query.
        Returns a list of dictionaries with text and metadata.
        """
        if self.vectorstore is None:
            logger.warning("RAG DB is not initialized. Cannot perform search.")
            return []
            
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=n_results)
            
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "text": doc.page_content,
                    "source": doc.metadata.get("source", "Unknown"),
                    "page": doc.metadata.get("page", -1),
                    "score": float(score)
                })
                    
            return formatted_results
        except Exception as e:
            logger.error(f"Error querying ChromaDB: {e}")
            return []

    def get_context_for_prompt(self, query: str, n_results: int = 4) -> str:
        """
        Searches the vector database and formats the results into a single string
        to be injected into an LLM prompt.
        """
        results = self.search(query, n_results=n_results)
        if not results:
            return ""
            
        context = "Here are relevant excerpts from the legal documents:\\n\\n"
        for i, res in enumerate(results):
            source_info = f"{os.path.basename(res['source'])} (Page {res['page']})"
            context += f"--- Excerpt {i+1} (Source: {source_info}) ---\\n"
            context += f"{res['text']}\\n\\n"
            
        return context
