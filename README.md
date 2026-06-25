# 🏛️ AI Legal Assistant - React & Python Full-Stack Platform

> **AI-powered legal guidance platform for Indian citizens using modern Indian legal references (BNS, BNSS, BSA) with multilingual support, powered by a React frontend and Python FastAPI backend.**

![Version](https://img.shields.io/badge/Version-2.0.0-blue) ![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen) ![License](https://img.shields.io/badge/License-MIT-green)

---

## ⚡ What This Is

A **complete production-ready full-stack application** designed to provide AI-powered legal guidance for Indian citizens. It features:
- 🤖 **Gemini AI** for automated legal analysis and document drafting.
- ⚖️ **Modern Indian Legal References** (Bharatiya Nyaya Sanhita - BNS, BNSS, BSA).
- 🌍 **6 Indian Languages** (English, Hindi, Tamil, Telugu, Malayalam, Kannada).
- 📱 **Professional React Frontend** styled with Tailwind CSS, Framer Motion, and Lucide React.
- 🚀 **Python FastAPI Backend** for high-performance async API endpoints.
- 🗄️ **Lightweight Local DB Persistence** using structured JSON.

---

## 🎯 Key Features

- **AI Legal Chatbot** - Interactive legal chat sessions supporting language translation and history persistence.
- **FIR Draft Generator** - A structured 3-step wizard to automatically compile professional First Information Reports (FIRs) incorporating relevant legal sections.
- **Crime Classification & IPC/BNS Mapping** - Automatically detects crime types and lists relevant sections of the Indian Penal Code (IPC) / Bharatiya Nyaya Sanhita (BNS).
- **PDF Generation & Downloader** - Formulates clean, formatted PDF documents of finalized FIRs with ReportLab, supporting Unicode characters.
- **Emergency Help Dashboard** - Quick access to emergency hotlines, procedures, and legal disclaimers.

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + Vite + Tailwind CSS + Framer Motion |
| **Backend** | Python 3.10+ + FastAPI + Uvicorn |
| **AI Integration** | Google GenAI SDK (Gemini 1.5 Flash) |
| **PDF Generation** | ReportLab (Python) |
| **Testing** | Playwright (E2E Integration Testing) |

---

## 📁 Project Structure

```
AI Legal Assistant/
├── frontend/                    # React SPA
│   ├── src/                     # Source code (Pages, Components, Services)
│   │   ├── pages/               # Chat, FIR Generator, My FIRs, Auth, Home
│   │   ├── services/api.js      # API axios wrapper
│   │   └── context/ChatContext  # Auth & Chat Session Context
│   ├── tests/e2e.spec.js        # Playwright E2E Flow tests
│   └── vite.config.js           # Dev server config & proxy
│
├── python_backend/              # Python FastAPI Backend
│   ├── main.py                  # Entrypoint, route handlers, AI & PDF generation
│   ├── database.json            # Local DB file (automatically created)
│   ├── test_api.py              # API Endpoint Integration tests
│   └── requirements.txt         # Backend Python Dependencies
│
├── start.bat                    # One-click startup script (Windows)
├── .env                         # Application Environment Variables
└── README.md                    # This file
```

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
1. **Python 3.10+** installed and added to PATH.
2. **Node.js 18+** and **npm** installed.
3. A **Google Gemini API Key** (Free from [Google AI Studio](https://aistudio.google.com/)).

### Easy One-Click Startup (Windows)
Double-click the **`start.bat`** file in the root folder. It will:
1. Start the FastAPI backend on `http://127.0.0.1:8000`.
2. Start the React dev server on `http://localhost:3000`.
3. Auto-open the application in your default browser.

---

### Manual Setup

#### 1. Setup Backend
```bash
cd python_backend
pip install -r requirements.txt
```

Create a `.env` file in the root directory and add your Gemini API Key:
```env
GEMINI_API_KEY=your_actual_api_key_here
API_HOST=127.0.0.1
API_PORT=8000
```

Start the backend:
```bash
python main.py
```

#### 2. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```
Open **`http://localhost:3000`** in your browser.

---

## 🧪 Testing

### Running Playwright End-to-End Tests
The repository is equipped with a Playwright script that tests the entire flow:
User Registration ➔ Step-by-Step FIR Generation ➔ Submit Draft ➔ View list & Select ➔ Finalize FIR ➔ PDF Verification.

```bash
cd frontend
npx playwright install
npx playwright test
```

---

## ⚖️ Legal Disclaimer

> ⚠️ **This platform provides LEGAL INFORMATION ONLY.**  
> It is **NOT** a substitute for professional counsel or a licensed advocate. Always consult a qualified attorney before taking formal legal action.
