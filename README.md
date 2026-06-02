# 🏛️ AI Legal Assistant - Professional Legal Guidance Platform

> **AI-powered legal guidance platform for Indian citizens using latest Indian legal references (BNS, BNSS, BSA) with multilingual support**

![Version](https://img.shields.io/badge/Version-2.0.0-blue) ![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen) ![License](https://img.shields.io/badge/License-MIT-green)

## ⚡ What This Is

A **complete full-stack application** providing AI-powered legal guidance specifically designed for Indian citizens. Uses:
- 🤖 **Gemini AI** for legal analysis
- ⚖️ **Modern Indian Legal References** (BNS, BNSS, BSA)
- 🌍 **6 Indian Languages** (English, Tamil, Hindi, Telugu, Malayalam, Kannada)
- 📱 **Professional React Frontend** with Tailwind CSS
- 🚀 **Production-Ready Node.js Backend**
- 📊 **MongoDB Database**

## 🎯 Key Features

✅ **AI Legal Chatbot** - Conversational guidance in your language  
✅ **FIR Generator** - Professional complaint documents  
✅ **Crime Detection** - Automatic classification with legal sections  
✅ **Multilingual** - 6 Indian languages with auto-detection  
✅ **Responsive Design** - Works on mobile, tablet, desktop  
✅ **Emergency Help** - Contact numbers & legal procedures  
✅ **Security** - Rate limiting, validation, CORS protection  
✅ **RAG Architecture** - Integration with existing Python backend (optional)  

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + Vite + Tailwind CSS + Framer Motion |
| **Backend** | Node.js + Express.js + MongoDB |
| **AI/LLM** | Gemini API + Axios |
| **Multilingual** | i18next + Custom Language Detection |
| **Security** | Helmet + CORS + Rate Limiting |
| **Database** | MongoDB + Mongoose |
| **Optional** | Python FastAPI (existing RAG pipeline)

## 📁 Project Structure

```
AI Legal Assistant/
├── frontend/                    # React SPA
│   ├── src/
│   │   ├── pages/              # 4 main pages
│   │   ├── components/         # Reusable components
│   │   ├── services/api.js     # API client
│   │   ├── context/            # Global state
│   │   ├── i18n/               # Multilingual
│   │   ├── App.jsx
│   │   └── index.css
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
│
├── backend/                     # Node.js Express API
│   ├── models/                 # MongoDB schemas
│   ├── controllers/            # Business logic
│   ├── routes/                 # API endpoints
│   ├── services/               # Core services
│   ├── middleware/             # Security & validation
│   ├── server.js
│   ├── .env
│   └── package.json
│
├── src/                        # Python RAG (existing)
│   ├── ingestion/
│   ├── retrieval/
│   ├── generation/
│   └── utils/
│
└── Documentation/
    ├── README.md               # This file
    ├── QUICKSTART.md           # 5-min setup
    ├── COMPLETE_DOCUMENTATION.md  # Full guide
    └── UPGRADE_REPORT.md       # Detailed changes
│   └── __init__.py
├── app/
│   └── streamlit_app.py       # (Coming soon) Frontend UI
├── notebooks/
│   └── experiment.ipynb       # (Coming soon) Testing notebook
├── requirements.txt           # ✅ Python dependencies
├── .env                       # ✅ Configuration template
├── .env.example              # (Coming soon) Example config
└── README.md                 # (You are here)
```

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- MongoDB (local or Atlas)
- Gemini API key (free from makersuite.google.com)

### Setup (5 minutes)

**Terminal 1 - Backend:**
```bash
cd backend
npm install
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
npm run dev  # Runs on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev  # Runs on http://localhost:3000
```

**Open Browser:** http://localhost:3000

> See [QUICKSTART.md](./QUICKSTART.md) for detailed setup with troubleshooting

## 📊 What's Included

### 🎨 Frontend Pages
- **Home** - Landing page with features
- **Chatbot** - AI legal chat (6 languages)
- **FIR Generator** - 4-step form with auto-generation
- **Emergency Help** - Contacts & procedures

### 🔌 Backend API (18 endpoints)
- Chat management (5 endpoints)
- FIR generation (7 endpoints)
- Legal information (4 endpoints)
- All with validation and rate limiting

### 🗄️ Database (5 models)
- User
- ChatSession
- FIRReport
- LegalDocument
- EvidenceChecklist

### 🤖 AI Services
- Crime category detection
- IPC/BNS section mapping
- FIR draft generation
- Evidence suggestion
- Text translation
- Language detection

## 🌍 Languages

Supports 6 Indian languages with automatic detection:
- 🇮🇳 English (en)
- 🇮🇳 Tamil (ta) - தமிழ்
- 🇮🇳 Hindi (hi) - हिन्दी
- 🇮🇳 Telugu (te) - తెలుగు
- 🇮🇳 Malayalam (ml) - മലയാളം
- 🇮🇳 Kannada (ka) - ಕನ್ನಡ

## 📖 Documentation

| Doc | Purpose |
|-----|---------|
| [QUICKSTART.md](./QUICKSTART.md) | 5-minute setup |
| [COMPLETE_DOCUMENTATION.md](./COMPLETE_DOCUMENTATION.md) | Full technical guide |
| [UPGRADE_REPORT.md](./UPGRADE_REPORT.md) | What changed in v2.0 |

## ⚖️ Legal Disclaimer

```
⚠️ This AI assistant provides LEGAL INFORMATION ONLY.
It is NOT a substitute for a licensed advocate.

Always consult a qualified legal professional before taking action.
```

## 🔒 Security

✅ CORS Protection  
✅ Rate Limiting  
✅ Input Validation  
✅ Error Handling  
✅ Helmet Security Headers  
✅ Environment Variable Protection  

## 🚢 Deployment

**Frontend:** Vercel, Netlify  
**Backend:** Railway, Render, Heroku  
**Database:** MongoDB Atlas  

## ✅ Continuous Integration

This repository includes a GitHub Actions workflow that runs frontend Playwright E2E tests and a backend finalize e2e script on pushes and PRs to `main`/`master`.

To run the Playwright e2e tests locally:

```bash
cd frontend
npx playwright install
npm run test:e2e
```

To run the backend finalize e2e locally:

```bash
cd backend
node test/finalize-e2e.js
```

## 📞 Support

- 📖 **Documentation:** See docs/ folder
- 🐛 **Issues:** Report via GitHub
- 💬 **Discussions:** GitHub Discussions

## 📈 Roadmap

- [ ] User Authentication
- [ ] PDF Download
- [ ] Voice Support
- [ ] Mobile App
- [ ] Video Consultations
- [ ] Payment Integration

## 📜 License

MIT License - See LICENSE file

---

**Status:** 🟢 Production Ready  
**Version:** 2.0.0  
**Last Updated:** May 29, 2026

```bash
# LLM Configuration
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_api_key_here
# OR
OPENAI_API_KEY=your_openai_key_here

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Vector Database
VECTOR_DB_TYPE=chromadb
CHROMADB_PATH=./data/chromadb

# Retrieval Settings
TOP_K_CHUNKS=5
SIMILARITY_THRESHOLD=0.5
OVERLAP_TOKENS=100
```

## Step 1: PDF Ingestion (Completed ✅)

### Processing Legal PDFs

Place your legal PDF files in `data/raw_pdfs/`:

```python
from src.ingestion.pdf_loader import LegalPDFLoader

# Load a single PDF
loader = LegalPDFLoader("data/raw_pdfs/supreme_court_judgment.pdf")
document = loader.load_document()

# Access metadata
print(f"Case: {document.metadata.case_name}")
print(f"Court: {document.metadata.court_name}")
print(f"Citation: {document.metadata.citation}")
print(f"IPC Sections: {document.metadata.ipc_sections}")
print(f"Judges: {document.metadata.judges}")

# Save to JSON
loader.save_to_json("data/processed/judgment.json")
```

### Batch Processing Multiple PDFs

```python
from src.ingestion.pdf_loader import batch_load_pdfs

processed = batch_load_pdfs(
    pdf_directory="data/raw_pdfs/",
    output_directory="data/processed/"
)
print(f"Processed {len(processed)} files")
```

## Step 2: Smart Chunking (Completed ✅)

### Chunk a Single Document

```python
from src.ingestion.chunker import LegalDocumentChunker
import json

# Load extracted document
with open("data/processed/judgment.json", 'r') as f:
    doc_data = json.load(f)

# Initialize chunker
chunker = LegalDocumentChunker(
    chunk_size=500,        # words per chunk
    chunk_overlap=100,     # overlapping words
    preserve_sections=True # don't split legal sections
)

# Chunk the document
chunks = chunker.chunk_document(
    text=doc_data['full_text'],
    metadata=doc_data['metadata'],
    page_contents=doc_data['page_contents']
)

# Each chunk contains:
# - chunk_id: Unique identifier
# - text: The actual content
# - ipc_sections: Extracted IPC references
# - case_citations: Extracted case citations
# - chunk_type: "judgment", "section", "order", etc.
# - page_numbers: Which pages in original PDF

print(f"Created {len(chunks)} chunks")
for chunk in chunks[:3]:
    print(f"\nChunk: {chunk.chunk_id}")
    print(f"Type: {chunk.chunk_type}")
    print(f"IPC Sections: {chunk.ipc_sections}")
    print(f"Citations: {chunk.case_citations}")
    print(f"Pages: {chunk.page_numbers}")
```

### Batch Chunking

```python
from src.ingestion.chunker import chunk_legal_documents_batch

all_chunks = chunk_legal_documents_batch(
    json_directory="data/processed/",
    output_directory="data/processed/chunks/",
    chunk_size=500,
    chunk_overlap=100
)
```

## Key Features of Current Implementation

### pdf_loader.py
- ✅ Extracts text from PDFs using PyMuPDF (with pdfplumber fallback)
- ✅ Preserves metadata: case name, court, date, judges, IPC sections
- ✅ Handles multi-column layouts
- ✅ Extracts tables from PDFs
- ✅ Uses regex to auto-detect citations and IPC sections
- ✅ Batch processing for multiple PDFs
- ✅ Structured JSON output for downstream processing

### chunker.py
- ✅ Intelligent chunking respecting legal section boundaries
- ✅ Sliding window overlap (configurable)
- ✅ Preserves IPC section references within chunks
- ✅ Auto-extracts IPC sections and citations per chunk
- ✅ Tags chunks with metadata (case_name, court, page numbers)
- ✅ Multiple chunking strategies (section-aware & simple)
- ✅ JSON export for vector store ingestion
- ✅ Batch processing for multiple documents

## Next Steps

### Step 3: Embedding & Vector Store
- Generate embeddings using sentence-transformers
- Store in ChromaDB with metadata filtering
- Add BM25 indexing for hybrid search

### Step 4: Hybrid Retrieval
- Combine dense + keyword search
- Implement Reciprocal Rank Fusion (RRF)
- Return top-5 relevant chunks with scores

### Step 5: LLM Integration
- Setup LangChain RAG chain
- Create legal-specific prompts
- Implement conversation memory

### Step 6: Citation Tracking
- Extract all citations from answers
- Link back to source documents
- Format citations properly (SCC, AIR, etc.)

### Step 7: Frontend UI
- Build Streamlit chat interface
- Add Hindi language support
- Display source citations
- Add court/date filtering

### Step 8: Evaluation
- Implement RAGAS metrics
- Measure citation accuracy
- Track faithfulness to retrieved documents

## Sample Legal Queries to Test

Once the full system is built, these queries will work:

1. "A person was arrested without a warrant. What are their rights under Indian law?"
2. "What IPC section applies if someone cheats me out of money online?"
3. "What does the Supreme Court say about bail in NDPS Act cases?"
4. "My landlord is illegally evicting me. What legal remedy do I have?"
5. "What is the punishment for domestic violence under Indian law?"

## Data Sources

Here are legitimate sources for Indian legal documents:

- **Indian Kanoon**: https://indiankanoon.org (has API & bulk downloads)
- **SCI Portal**: https://sci.gov.in (Supreme Court judgments)
- **High Court Websites**: Each high court has judgment portals
- **SCAAP Database**: Central database of court judgments
- **Public Domain**: Many older judgments are in public domain

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | anthropic | Which LLM to use (anthropic/openai) |
| `CHUNK_SIZE` | 500 | Words per chunk |
| `CHUNK_OVERLAP` | 100 | Overlapping words between chunks |
| `TOP_K_CHUNKS` | 5 | Number of chunks to retrieve |
| `SIMILARITY_THRESHOLD` | 0.5 | Min similarity for chunk retrieval |

## Common Issues & Solutions

### Issue: PyMuPDF not installing
```bash
# Windows users might need:
pip install --upgrade pymupdf
```

### Issue: pdfplumber not working on some PDFs
```python
# Specify use_pdfplumber=False for problematic PDFs
loader = LegalPDFLoader("file.pdf")
text, pages = loader.extract_text(use_pdfplumber=False)
```

### Issue: Unicode characters in PDF
```bash
# Make sure you're using UTF-8 encoding
export PYTHONIOENCODING=utf-8
```

## Legal Disclaimer

⚠️ **This tool is for educational and reference purposes only.**
- **NOT a substitute for professional legal advice**
- Always consult with a qualified lawyer
- Outputs may contain inaccuracies or hallucinations
- Users are responsible for verifying all information

## Contributing

Contributions welcome! Areas for improvement:
- Better Hindi language support
- Integration with Indian Kanoon API
- Voice input with Whisper
- PDF export with proper formatting
- Performance optimizations

## License

MIT License - See LICENSE file for details

## Authors

Developed as a comprehensive RAG system for Indian legal research.

## Support

For issues, questions, or suggestions:
- Check the notebooks/ folder for examples
- Review the inline code documentation
- Test with sample PDFs in data/raw_pdfs/

---

**Next Milestone**: Ready for Step 3 (Embedding & Vector Store integration)

Confirm to proceed! 🚀
