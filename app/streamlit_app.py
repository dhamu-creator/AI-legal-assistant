"""
AI Legal Assistant - Streamlit UI
Full-featured web interface for Indian legal QA system with RAG pipeline
Supports multi-turn conversations, citation extraction, and PDF export
"""

import streamlit as st
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import logging

# Load environment variables from .env file
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import backend components
try:
    from src.ingestion.embedder import LegalEmbedder
    from src.retrieval.vector_store import ChromaDBStore, load_and_index_chunks
    from src.generation.llm_chain import LegalRAGChain
    from src.utils.citation_tracker import CitationExtractor, CitationFormatter
except ImportError as e:
    logger.error(f"Import error (core): {e}")
    st.error(f"Failed to import core modules: {e}")

# Try multilingual imports with fallback
try:
    from src.utils.multilingual_support import (
        Language,
        LanguageDetector,
        MultilingualAssistant
    )
    HAS_MULTILINGUAL = True
except ImportError as e:
    logger.warning(f"Multilingual support unavailable: {e}")
    HAS_MULTILINGUAL = False
    # Define a simple Language enum fallback
    class LanguageValue:
        def __init__(self, val):
            self.value = val
    
    class Language:
        ENGLISH = LanguageValue("en")
        HINDI = LanguageValue("hi")
        TAMIL = LanguageValue("ta")

# Streamlit Configuration
st.set_page_config(
    page_title="⚖️ AI Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .citation-badge {
        display: inline-block;
        background-color: #e8f4f8;
        color: #0066cc;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        margin-right: 0.5rem;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .source-card {
        background-color: #f8f9fa;
        border-left: 4px solid #0066cc;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .confidence-high {
        color: #28a745;
    }
    .confidence-medium {
        color: #ffc107;
    }
    .confidence-low {
        color: #dc3545;
    }
    .disclaimer {
        background-color: #fff3cd;
        border-left: 4px solid #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

@st.cache_resource
def initialize_backend():
    """Initialize RAG chain and components (cached for performance)"""
    errors = []
    
    try:
        # Get LLM provider from environment
        llm_provider = os.getenv("LLM_PROVIDER", "groq").lower()
        logger.info(f"Using LLM provider: {llm_provider}")

        # Get appropriate API key based on provider
        if llm_provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                try:
                    api_key = st.secrets.get("GROQ_API_KEY")
                except:
                    api_key = None
        elif llm_provider == "google":
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                try:
                    api_key = st.secrets.get("GEMINI_API_KEY")
                except:
                    api_key = None
        elif llm_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                try:
                    api_key = st.secrets.get("OPENAI_API_KEY")
                except:
                    api_key = None
        else:
            # Unsupported provider — fall back to groq
            logger.warning(f"Unknown LLM_PROVIDER '{llm_provider}', falling back to groq.")
            llm_provider = "groq"
            api_key = os.getenv("GROQ_API_KEY")

        if not api_key or api_key.startswith("your"):
            errors.append(
                f"No valid API key configured for provider '{llm_provider}'. "
                "Please set GROQ_API_KEY in your .env file."
            )
            logger.warning(f"API Key Error: {errors[-1]}")
            return None, None, errors
        
        logger.info(f"✓ API key found for {llm_provider}")
        
        # Check if data directory exists
        data_path = Path("./data/chromadb")
        if not data_path.exists():
            errors.append("No vector store found at ./data/chromadb")
            logger.warning(f"Data Error: {errors[-1]}")
            return None, None, errors
        
        logger.info("✓ Vector store directory exists")
        
        # Initialize vector store
        try:
            vector_store = ChromaDBStore("./data/chromadb")
            logger.info("✓ ChromaDBStore initialized")
        except Exception as e:
            errors.append(f"Vector store initialization failed: {str(e)}")
            logger.error(f"Vector Store Error: {errors[-1]}")
            return None, None, errors
        
        # Try to initialize embedder (with fallback for HuggingFace issues)
        embedder = None
        try:
            logger.info("Attempting to initialize embedder...")
            embedder = LegalEmbedder()
            logger.info("✓ LegalEmbedder initialized")
        except Exception as e:
            logger.warning(f"Embedder initialization fallback: {str(e)}")
            # We can still work with BM25-only search if embedder fails
            embedding_warning = f"Dense search unavailable (embedder failed): {str(e)}"
            errors.append(embedding_warning)
            logger.warning(embedding_warning)
        
        # Initialize retriever with pre-computed embeddings and chunks
        try:
            # Load chunks and create hybrid retriever
            retriever = load_and_index_chunks(
                "data/processed/chunks/embedded",
                vector_store,
                embedder  # Can be None, falls back to BM25
            )
            logger.info("✓ Retriever initialized (hybrid search ready)")
        except Exception as e:
            errors.append(f"Retriever initialization failed: {str(e)}")
            logger.error(f"Retriever Error: {errors[-1]}")
            return None, None, errors
        
        # Initialize RAG chain with the selected provider
        try:
            chain = LegalRAGChain(
                retriever=retriever,
                llm_provider=llm_provider,
                temperature=0.2,
                use_conversation_memory=True
            )
            logger.info("✓ LegalRAGChain initialized")
        except Exception as e:
            errors.append(f"RAG Chain initialization failed: {str(e)}")
            logger.error(f"RAG Chain Error: {errors[-1]}")
            return None, None, errors
        
        # Initialize multilingual assistant if available
        multilingual_assistant = None
        if HAS_MULTILINGUAL:
            try:
                multilingual_assistant = MultilingualAssistant(chain)
                logger.info("✓ Multilingual assistant initialized")
            except Exception as e:
                logger.warning(f"Multilingual assistant not available: {e}")
        
        logger.info("✅ BACKEND FULLY INITIALIZED")
        return chain, multilingual_assistant, errors  # Return errors even on success for warnings

    except Exception as e:
        import traceback
        error_msg = f"Unexpected error: {str(e)}"
        errors.append(error_msg)
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return None, None, errors


def initialize_session_state():
    """Initialize Streamlit session state"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None
    
    if "multilingual_assistant" not in st.session_state:
        st.session_state.multilingual_assistant = None
    
    if "init_errors" not in st.session_state:
        st.session_state.init_errors = []
    
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "English"
    
    if "filters" not in st.session_state:
        st.session_state.filters = {
            "court": None,
            "ipc_section": None,
            "year_range": None
        }
    
    if "search_results" not in st.session_state:
        st.session_state.search_results = []


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_citation_badges(citations: List[str]) -> str:
    """Format citations as HTML badges"""
    if not citations:
        return "No citations extracted"
    
    badges = "".join([f'<span class="citation-badge">{c}</span>' for c in citations])
    return badges


def format_confidence(score: float) -> Tuple[str, str]:
    """Format confidence score with color indicator"""
    percentage = score * 100
    
    if score >= 0.8:
        return f"🟢 High ({percentage:.0f}%)", "confidence-high"
    elif score >= 0.5:
        return f"🟡 Medium ({percentage:.0f}%)", "confidence-medium"
    else:
        return f"🔴 Low ({percentage:.0f}%)", "confidence-low"


def display_sources(sources: List[Dict], max_display: int = 3) -> None:
    """Display retrieved source documents"""
    st.markdown("### 📄 Retrieved Sources")
    
    if not sources:
        st.info("No sources retrieved.")
        return
    
    for i, source in enumerate(sources[:max_display], 1):
        with st.container():
            st.markdown(
                f"""
                <div class="source-card">
                    <strong>📋 Source {i}: {source.get('case_name', 'Unknown')}</strong><br>
                    <small>
                        Court: {source.get('court', 'N/A')} | 
                        Year: {source.get('year', 'N/A')} | 
                        Relevance: {source.get('relevance_score', 0):.2%}
                    </small>
                    <p style="margin-top: 0.5rem; color: #666;">
                        {source.get('text', '')[:200]}...
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    if len(sources) > max_display:
        st.caption(f"... and {len(sources) - max_display} more sources")


def display_legal_disclaimer() -> None:
    """Display legal disclaimer"""
    st.markdown(
        """
        <div class="disclaimer">
            <strong>⚠️ Legal Disclaimer:</strong><br>
            This AI Assistant provides general legal information for educational purposes only. 
            It is NOT a substitute for professional legal advice. 
            Always consult with a qualified lawyer for specific legal matters. 
            The information provided may contain inaccuracies. 
            <strong>User responsibility:</strong> Verify all information with authoritative sources.
        </div>
        """,
        unsafe_allow_html=True
    )


def export_conversation_to_json(chat_history: List[Dict]) -> str:
    """Export conversation to JSON format"""
    export_data = {
        "conversation_id": st.session_state.conversation_id,
        "timestamp": datetime.now().isoformat(),
        "messages": chat_history,
        "language": st.session_state.selected_language
    }
    return json.dumps(export_data, indent=2, ensure_ascii=False)


# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

def render_sidebar() -> None:
    """Render sidebar with settings and options"""
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        
        # Search Section
        st.markdown("### 🔎 Document Search")
        search_query = st.text_input(
            "Search documents:",
            placeholder="e.g., Section 302, murder, punishment",
            key="search_query"
        )
        
        if search_query and st.session_state.rag_chain:
            if st.button("🔍 Search"):
                try:
                    results = st.session_state.rag_chain.retriever.search(
                        search_query,
                        top_k=5
                    )
                    st.session_state.search_results = results
                    st.success(f"Found {len(results)} results!")
                except Exception as e:
                    st.error(f"Search error: {e}")
        
        # Display search results if available
        if st.session_state.get("search_results"):
            st.markdown("#### Search Results")
            for i, result in enumerate(st.session_state.search_results, 1):
                with st.expander(f"Result {i}: {result.get('title', 'Document')}"):
                    st.markdown(result.get("content", ""))
                    if result.get("metadata"):
                        st.caption(f"Source: {result['metadata']}")
        
        st.markdown("---")
        
        # Language Selection
        st.markdown("### 🌐 Language")
        language_options = {
            "English 🇬🇧": Language.ENGLISH.value,
            "हिंदी (Hindi) 🇮🇳": Language.HINDI.value,
            "தமிழ் (Tamil) 🇮🇳": Language.TAMIL.value,
        }
        
        selected_lang_display = st.selectbox(
            "Select Language:",
            list(language_options.keys()),
            key="language_select"
        )
        st.session_state.selected_language = language_options[selected_lang_display]
        
        # Filters
        st.markdown("### 🔍 Filters")
        st.session_state.filters["court"] = st.selectbox(
            "Court:",
            ["All", "Supreme Court", "High Court", "District Court"],
            key="filter_court"
        )
        
        st.session_state.filters["ipc_section"] = st.text_input(
            "IPC Section (e.g., 302):",
            key="filter_ipc"
        )
        
        # Conversation Controls
        st.markdown("### 💬 Conversation")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear History"):
                st.session_state.chat_history = []
                if st.session_state.rag_chain:
                    st.session_state.rag_chain.clear_memory()
                st.success("History cleared!")
        
        with col2:
            if st.button("📥 Export"):
                json_export = export_conversation_to_json(st.session_state.chat_history)
                st.download_button(
                    label="Download JSON",
                    data=json_export,
                    file_name=f"legal_chat_{st.session_state.conversation_id}.json",
                    mime="application/json"
                )
        
        # System Stats
        st.markdown("### 📊 System Stats")
        st.caption(f"Session ID: `{st.session_state.conversation_id[:8]}...`")
        st.caption(f"Messages: {len(st.session_state.chat_history)}")
        
        if st.session_state.rag_chain:
            memory_summary = st.session_state.rag_chain.get_memory_summary()
            st.caption(f"Memory: {memory_summary.get('total_turns', 0)} turns")
        
        # About
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info(
            """
            **AI Legal Assistant v2.0**

            Built with:
            - LangChain for RAG orchestration
            - ChromaDB for vector storage
            - Groq (Llama 3.3-70B) for generation
            - Hybrid search (dense + BM25)
            - Multilingual support (EN/HI/TA)

            **Project:** Indian Legal QA System
            """
        )


# ============================================================================
# MAIN CHAT INTERFACE
# ============================================================================

def render_chat_interface() -> None:
    """Main chat interface"""
    
    # Display legal disclaimer
    display_legal_disclaimer()
    
    # Chat messages container
    st.markdown("## 💬 Chat")
    
    # Display chat history
    chat_container = st.container(height=400)
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Display citations if available
                if message.get("citations"):
                    st.markdown("**Citations:**")
                    st.markdown(
                        format_citation_badges(message["citations"]),
                        unsafe_allow_html=True
                    )
                
                # Display confidence if available
                if message.get("confidence_score"):
                    conf_text, conf_class = format_confidence(message["confidence_score"])
                    st.markdown(f'<p class="{conf_class}">{conf_text}</p>', unsafe_allow_html=True)
                
                # Display sources if available
                if message.get("sources"):
                    with st.expander("📄 View Sources"):
                        display_sources(message["sources"])
    
    # Input area
    st.markdown("---")
    
    # Input with columns for better layout
    col1, col2 = st.columns([0.85, 0.15])
    
    with col1:
        user_input = st.text_input(
            "Ask your legal question...",
            placeholder="E.g., What is Section 302 IPC? What is the punishment for cheating?",
            key="user_input"
        )
    
    with col2:
        send_button = st.button("📤 Send", use_container_width=True)
    
    # Process user query
    if send_button and user_input:
        process_query(user_input)


def process_query(query: str) -> None:
    """Process user query through RAG chain with multilingual support"""
    
    # Initialize chain if needed
    if not st.session_state.rag_chain or not st.session_state.multilingual_assistant:
        result = initialize_backend()
        if isinstance(result, tuple) and len(result) == 3:
            st.session_state.rag_chain, st.session_state.multilingual_assistant, _ = result
        elif isinstance(result, tuple) and len(result) >= 2:
            st.session_state.rag_chain, st.session_state.multilingual_assistant = result[:2]
    
    if not st.session_state.rag_chain or not st.session_state.multilingual_assistant:
        st.error("❌ RAG chain not initialized. Check API key and backend setup.")
        return
    
    # Add user message to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": query
    })
    
    # Show loading indicator
    with st.spinner("⏳ Generating answer..."):
        try:
            # Determine target language
            language_map = {
                "en": Language.ENGLISH,
                "hi": Language.HINDI,
                "ta": Language.TAMIL,
            }
            
            target_lang = language_map.get(st.session_state.selected_language, Language.ENGLISH)
            
            # Query multilingual assistant
            multilingual_response = st.session_state.multilingual_assistant.query(
                question=query,
                target_language=target_lang,
                top_k=5
            )
            
            # Prepare response message
            response_message = {
                "role": "assistant",
                "content": multilingual_response.translated_response,
                "english_content": multilingual_response.english_response,
                "citations": multilingual_response.citations,
                "sources": multilingual_response.sources,
                "language": target_lang.name
            }
            
            # Add to chat history
            st.session_state.chat_history.append(response_message)
            
            st.success("✅ Response generated!")
        
        except Exception as e:
            error_msg = f"❌ Error processing query: {str(e)}"
            logger.error(error_msg)
            st.error(error_msg)
            
            # Remove the user message if processing failed
            if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
                st.session_state.chat_history.pop()


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main Streamlit app"""
    
    # Page header
    st.markdown("# ⚖️ AI Legal Assistant for Indian Courts")
    st.markdown(
        "Powered by RAG • Ask questions about Indian Law, IPC, Acts, and Legal Procedures"
    )
    st.markdown("---")
    
    # Initialize session state
    initialize_session_state()
    
    # Try to initialize backend
    if st.session_state.rag_chain is None:
        result = initialize_backend()
        if len(result) == 3:
            chain, assistant, errors = result
            st.session_state.rag_chain = chain
            st.session_state.multilingual_assistant = assistant
            st.session_state.init_errors = errors
        else:
            # Fallback for old return format
            if isinstance(result, tuple) and len(result) >= 2:
                st.session_state.rag_chain, st.session_state.multilingual_assistant = result[:2]
            st.session_state.init_errors = []
    
    # Check if backend is ready
    if st.session_state.rag_chain is None:
        # Show setup page with debug info
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.warning("⚠️ **Backend Not Ready**")
            
            # Show errors if any
            if st.session_state.get("init_errors"):
                st.error("**Initialization Errors:**")
                for error in st.session_state.init_errors:
                    st.error(f"• {error}")
            
            st.markdown("""
            The AI Legal Assistant needs to be configured before use. Follow these steps:
            
            ### 1️⃣ Set Up API Key
            Add your Groq API key to `.streamlit/secrets.toml`:
            ```toml
            GROQ_API_KEY = "your-groq-api-key-here"
            ```
            
            Or set it as an environment variable:
            ```powershell
            $env:GROQ_API_KEY="your-groq-api-key-here"
            ```
            
            ### 2️⃣ Add Legal Documents
            Place your legal PDF documents in:
            ```
            data/raw_pdfs/
            ```
            
            ### 3️⃣ Process Documents
            Run the ingestion pipeline:
            ```bash
            python quickstart.py
            ```
            
            This will extract, chunk, embed, and index your documents.
            
            ### 4️⃣ Restart the App
            Once setup is complete, refresh this page.
            """)
        
        with col2:
            st.info("""
            ### 📚 About

            **AI Legal Assistant v2.0**

            Built with:
            - LangChain for RAG
            - ChromaDB for vectors
            - Groq (Llama 3.3-70B) for generation
            - Hybrid search (dense + BM25)
            - Multilingual support (EN/HI/TA)

            📖 See docs for more info
            """)
    else:
        # Show normal app
        render_sidebar()
        render_chat_interface()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.85rem;'>
            Built with ❤️ using Streamlit | 
            <a href='https://github.com/'>GitHub</a> | 
            <a href='https://doc.com/'>Docs</a>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
