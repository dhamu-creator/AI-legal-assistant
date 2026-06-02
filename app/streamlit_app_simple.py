"""
AI Legal Assistant - Streamlit UI (Simplified Demo)
Lightweight version that launches immediately
"""

import streamlit as st
from datetime import datetime
from pathlib import Path

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
    .setup-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
    }
    .setup-card h1 {
        margin-top: 0;
    }
    .code-block {
        background-color: #f5f5f5;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: monospace;
        margin: 1rem 0;
        overflow-x: auto;
    }
    .disclaimer {
        background-color: #fff3cd;
        border-left: 4px solid #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .feature-list {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    }
    .feature-item {
        background-color: #f0f7ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0066cc;
    }
</style>
""", unsafe_allow_html=True)

# Main Title
st.markdown("# ⚖️ AI Legal Assistant for Indian Courts")
st.markdown("*Powered by RAG • Ask questions about Indian Law, IPC, Acts, and Legal Procedures*")
st.divider()

# Two column layout
col1, col2 = st.columns([2, 1])

with col1:
    # Setup Instructions
    st.markdown("""
    ## 🚀 Getting Started
    
    Your AI Legal Assistant is ready to be configured! Follow these simple steps:
    
    ### Step 1️⃣: Set Your API Key
    
    Choose one of these options:
    
    **Option A: Environment Variable (Recommended)**
    ```bash
    set ANTHROPIC_API_KEY=sk-ant-...
    ```
    
    **Option B: Secrets File**
    
    Edit `.streamlit/secrets.toml`:
    """)
    
    st.code("""ANTHROPIC_API_KEY = "sk-ant-..."
OPENAI_API_KEY = "sk-..."  # Optional""", language="toml")
    
    st.markdown("""
    > Get your API key from [Anthropic Console](https://console.anthropic.com)
    
    ### Step 2️⃣: Add Legal Documents
    
    Place your legal PDFs in this folder:
    """)
    
    st.code("data/raw_pdfs/", language="text")
    
    st.markdown("""
    You can use any Indian legal documents:
    - Court judgments
    - IPC sections
    - Legal acts and rules
    - Constitution excerpts
    
    ### Step 3️⃣: Process Documents
    
    Run the ingestion pipeline:
    """)
    
    st.code("python quickstart.py", language="bash")
    
    st.markdown("""
    This will:
    1. ✅ Extract text from PDFs
    2. ✅ Split into smart chunks
    3. ✅ Generate embeddings  
    4. ✅ Index in vector database
    
    ### Step 4️⃣: Restart & Chat
    
    Once complete, restart the app:
    """)
    
    st.code("streamlit run app/streamlit_app.py", language="bash")

with col2:
    st.markdown("## ℹ️ About This System")
    
    st.info("""
    ### 📦 Built With
    
    - **LangChain**: RAG orchestration
    - **ChromaDB**: Vector database
    - **Claude**: Legal AI model
    - **Streamlit**: Web interface
    
    ### 🌐 Languages
    - English 🇮🇳
    - हिंदी (Hindi)
    - தமிழ் (Tamil)
    
    ### 🔍 Features
    - Hybrid search (dense + keyword)
    - Citation extraction
    - Multi-turn conversations
    - Session export
    - Legal entity recognition
    """)
    
    st.markdown("---")
    st.markdown("""
    ### 📚 Resources
    
    - [GitHub Repository](https://github.com)
    - [Documentation](https://docs.example.com)
    - [Anthropic Docs](https://docs.anthropic.com)
    """)

# Demo Section
st.divider()
st.markdown("## 💬 Live Demo (Without Documents)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Ask a Legal Question")
    sample_questions = [
        "What is Section 302 of IPC?",
        "What is the right to privacy under Article 21?",
        "Difference between bail and bond",
        "What is criminal negligence under IPC?"
    ]
    
    selected_q = st.selectbox("Try one of these questions:", sample_questions)
    
    if st.button("📤 Submit", use_container_width=True):
        st.info("""
        ℹ️ **Demo Mode**: This is a preview of the chat interface.
        
        To enable full functionality:
        1. Set up your API key (see left panel)
        2. Add legal documents
        3. Run the ingestion pipeline
        4. Restart the app
        """)

with col2:
    st.markdown("### System Status")
    st.metric("Backend Status", "⏳ Awaiting Setup")
    st.metric("Vector Store", "Empty")
    st.metric("API Key", "Not Set")
    st.metric("Documents", "0")

# Footer  
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.85rem;'>
    <p>Built with ❤️ using Streamlit | 
    <a href='https://github.com'>GitHub</a> | 
    <a href='/'>Home</a></p>
    <p style='margin-top: 1rem; font-size: 0.75rem;'>
        © 2026 AI Legal Assistant | For educational purposes
    </p>
</div>
""", unsafe_allow_html=True)
