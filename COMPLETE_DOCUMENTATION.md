# AI Legal Assistant - Complete Project Documentation

## 📋 Project Overview

This is a **professional, production-ready AI-powered legal guidance platform** designed specifically for Indian citizens. It provides:

- **AI Legal Chatbot**: Conversational legal guidance in multiple Indian languages
- **FIR/Complaint Generator**: Automated generation of professional FIR and complaint documents
- **Legal Information Database**: IPC, BNS, BNSS, BSA, and cyber law references
- **Evidence Checklist**: Dynamic evidence suggestions based on crime type
- **Emergency Contacts & Procedures**: Step-by-step legal procedures and emergency numbers
- **Multilingual Support**: 6 Indian languages (English, Tamil, Hindi, Telugu, Malayalam, Kannada)
- **RAG Pipeline**: Retrieval-Augmented Generation for accurate legal information

---

## 🏗️ Architecture Overview

### Tech Stack

**Frontend:**
- React 18 with Vite
- Tailwind CSS for styling
- Framer Motion for animations
- Axios for API calls
- React Router for navigation
- i18next for multilingual support
- Heroicons for UI icons

**Backend:**
- Node.js + Express.js
- MongoDB with Mongoose
- Gemini AI API for LLM
- Rate limiting, CORS, helmet for security
- Winston for logging
- Nodemon for development

**Infrastructure:**
- MongoDB Atlas (cloud) or local MongoDB
- Python FastAPI (existing RAG backend - can be integrated)
- Docker support (optional)

### Project Structure

```
AI Legal Assistant/
│
├── frontend/                          # React Frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx              # Landing page
│   │   │   ├── Chatbot.jsx           # AI chat interface
│   │   │   ├── FIRGenerator.jsx      # FIR generation
│   │   │   ├── EmergencyHelp.jsx     # Emergency info
│   │   ├── components/                # Reusable React components
│   │   ├── services/
│   │   │   └── api.js                # API client
│   │   ├── context/
│   │   │   └── ChatContext.jsx       # Global state management
│   │   ├── i18n/
│   │   │   └── config.js             # Internationalization
│   │   ├── App.jsx                   # Main app component
│   │   ├── index.jsx                 # React entry point
│   │   └── index.css                 # Global styles
│   ├── index.html                    # HTML template
│   ├── vite.config.js                # Vite configuration
│   ├── tailwind.config.js            # Tailwind configuration
│   ├── postcss.config.js             # PostCSS configuration
│   └── package.json                  # Frontend dependencies
│
├── backend/                           # Node.js/Express Backend
│   ├── models/
│   │   ├── User.js                   # User schema
│   │   ├── ChatSession.js            # Chat history
│   │   ├── FIRReport.js              # FIR records
│   │   ├── LegalDocument.js          # Legal references
│   │   └── EvidenceChecklist.js      # Evidence data
│   ├── controllers/
│   │   ├── ChatController.js         # Chat endpoints
│   │   └── FIRController.js          # FIR endpoints
│   ├── routes/
│   │   ├── chatRoutes.js             # Chat API routes
│   │   ├── firRoutes.js              # FIR API routes
│   │   └── legalRoutes.js            # Legal info routes
│   ├── services/
│   │   ├── AIService.js              # Gemini API integration
│   │   ├── ChatService.js            # Chat logic
│   │   ├── FIRService.js             # FIR generation
│   │   └── LanguageDetectionService.js # Language detection
│   ├── middleware/
│   │   ├── errorHandler.js           # Error handling
│   │   ├── validation.js             # Input validation
│   │   ├── rateLimit.js              # Rate limiting
│   │   └── logging.js                # Request logging
│   ├── config/
│   │   └── db.js                     # MongoDB connection
│   ├── server.js                     # Express server
│   ├── .env                          # Environment variables
│   ├── .env.example                  # Example env file
│   └── package.json                  # Backend dependencies
│
├── src/ (existing Python)             # Keep for RAG integration
│   ├── ingestion/
│   ├── retrieval/
│   ├── generation/
│   └── utils/
│
└── README.md                          # Project documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
- Node.js 16+ and npm
- MongoDB (local or Atlas)
- Python 3.9+ (for existing RAG backend)
- Git

### Step 1: Clone the Repository

```bash
cd "c:\placement project\AI Legel Assistant"
```

### Step 2: Backend Setup

```bash
cd backend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Update .env with your API keys
# MONGO_URI=your_mongodb_connection
# GEMINI_API_KEY=your_gemini_key
# etc.

# Start backend server
npm run dev
# Runs on http://localhost:5000
```

### Step 3: Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
# Runs on http://localhost:3000
```

### Step 4: Open in Browser

Visit `http://localhost:3000` in your browser.

---

## 📡 API Endpoints

### Chat Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/session` | Create new chat session |
| POST | `/api/chat/message` | Send message & get response |
| GET | `/api/chat/history/:sessionId` | Get chat history |
| GET | `/api/chat/sessions/:userId` | Get all user sessions |
| DELETE | `/api/chat/session/:sessionId` | Delete chat session |

### FIR Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/fir/create/:userId` | Create FIR report |
| POST | `/api/fir/generate/:userId` | Generate FIR draft |
| GET | `/api/fir/user/:userId` | Get user's FIRs |
| GET | `/api/fir/:firId` | Get specific FIR |
| PUT | `/api/fir/:firId` | Update FIR |
| DELETE | `/api/fir/:firId` | Delete FIR |
| POST | `/api/fir/evidence/checklist` | Get evidence checklist |
| GET | `/api/fir/pdf/:firId` | Generate PDF (planning) |

### Legal Info Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/legal/languages` | Get supported languages |
| GET | `/api/legal/crime-categories` | Get crime types |
| GET | `/api/legal/disclaimer` | Get disclaimer |
| GET | `/api/legal/emergency-contacts` | Get emergency numbers |

---

## 🌍 Multilingual Support

The platform supports **6 Indian languages**:

1. **English (en)** - Default
2. **Tamil (ta)** - தமிழ்
3. **Hindi (hi)** - हिन्दी
4. **Telugu (te)** - తెలుగు
5. **Malayalam (ml)** - മലയാളം
6. **Kannada (ka)** - ಕನ್ನಡ

### Language Detection

The system automatically detects the user's language using Unicode character ranges. When a message is sent:

1. **Detect Language**: Analyze Unicode characters to identify the language
2. **Translate to English**: Convert non-English text to English for AI processing
3. **Process**: Analyze the legal issue
4. **Translate Back**: Return response in the user's preferred language
5. **Maintain Accuracy**: Preserve IPC/BNS section names

---

## 🤖 AI Integration

### Gemini AI Setup

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env`:
   ```
   GEMINI_API_KEY=your_key_here
   ```

### AI Features

- **Crime Category Detection**: Automatically identifies type of crime
- **IPC/BNS Section Mapping**: Suggests relevant legal sections
- **Legal Guidance**: Provides procedural guidance
- **FIR Generation**: Creates professional FIR documents
- **Evidence Suggestion**: Recommends what evidence to collect
- **Multi-turn Conversations**: Maintains context across messages

---

## 📊 Database Schema

### User Model
```javascript
{
  name: String,
  email: String (unique),
  phone: String,
  language: String (enum),
  savedReports: [ObjectId], // References to FIRReport
  chatSessions: [ObjectId], // References to ChatSession
  preferences: {
    darkMode: Boolean,
    notifications: Boolean
  },
  createdAt: Date,
  updatedAt: Date
}
```

### ChatSession Model
```javascript
{
  userId: ObjectId,
  title: String,
  messages: [{
    role: String (user/assistant),
    content: String,
    language: String,
    detectedCrimeCategory: String,
    relevantIPCSection: String,
    sourceDocuments: [String],
    createdAt: Date
  }],
  crimeCategory: String,
  ipcSections: [String],
  bnsSections: [String],
  isResolved: Boolean,
  createdAt: Date,
  updatedAt: Date
}
```

### FIRReport Model
```javascript
{
  userId: ObjectId,
  title: String,
  incidentDetails: String,
  incidentDate: Date,
  incidentLocation: String,
  crimeCategory: String (enum),
  ipcSections: [String],
  bnsSections: [String],
  complainantDetails: {
    name, phone, address, email
  },
  suspectDetails: {
    name, description, address
  },
  witnessDetails: [{
    name, phone, statement
  }],
  evidence: [String],
  firDraft: String,
  status: String (draft/submitted/filed),
  language: String,
  createdAt: Date,
  updatedAt: Date
}
```

---

## 🔒 Security Features

### Implemented
- **Helmet**: HTTP header protection
- **CORS**: Cross-origin resource sharing control
- **Rate Limiting**: Prevent API abuse (100 requests per 15 min for chat)
- **Input Validation**: Sanitize user inputs
- **Error Handling**: Centralized error management
- **Environment Variables**: Secure API key management
- **MongoDB**: Password protection

### To Add
- **JWT Authentication**: User session management
- **HTTPS**: SSL/TLS encryption
- **Data Encryption**: Encrypt sensitive data at rest
- **OWASP Compliance**: Follow security best practices

---

## 🎯 Crime Categories Supported

1. **Theft** - Stealing of property
2. **Robbery** - Theft with force/intimidation
3. **CyberFraud** - Online fraud, phishing
4. **Harassment** - Verbal/physical harassment
5. **DomesticViolence** - Violence within family
6. **Blackmail** - Extortion, blackmail
7. **OnlineScams** - Scams via internet
8. **IdentityTheft** - Unauthorized identity use
9. **FinancialFraud** - Financial fraud cases
10. **PhysicalAssault** - Physical violence

---

## 📱 Responsive Design

The frontend is fully responsive:
- **Desktop**: Full featured interface (1024px+)
- **Tablet**: Optimized layout (768px - 1023px)
- **Mobile**: Mobile-friendly UI (< 768px)

---

## 🚢 Deployment

### Frontend Deployment (Vercel/Netlify)

```bash
cd frontend
npm run build
# Deploy 'dist' folder to Vercel/Netlify
```

### Backend Deployment (Heroku/Railway/Render)

```bash
cd backend
npm start
# Ensure MONGO_URI and API keys are set in environment
```

### MongoDB Setup

1. **Local**: `mongodb://localhost:27017/ai-legal-assistant`
2. **Atlas (Cloud)**: Get connection string from MongoDB Atlas console

---

## 📝 Important Disclaimers

⚠️ **This application displays the following disclaimer everywhere:**

> "This AI assistant provides legal information and guidance only. It is not a substitute for a licensed advocate. Always consult with a qualified legal professional before taking action."

---

## 🛠️ Development

### Running in Development Mode

Terminal 1 - Backend:
```bash
cd backend
npm run dev
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

### Building for Production

Backend:
```bash
cd backend
npm start
```

Frontend:
```bash
cd frontend
npm run build
npm run preview
```

---

## 📚 Future Enhancements

1. **Voice Support**: Speech-to-text and text-to-speech in Indian languages
2. **PDF Generation**: Download FIR and reports as PDF
3. **User Authentication**: JWT-based user login/signup
4. **Payment Integration**: For premium legal consultations
5. **Lawyer Matching**: Connect users with qualified lawyers
6. **Mobile App**: iOS and Android native apps
7. **Advanced RAG**: Better legal document retrieval
8. **Legal Case Tracking**: Track case progress
9. **Community Forum**: User discussions and advice
10. **Video Consultations**: Schedule video calls with lawyers

---

## 📞 Support

For issues, questions, or contributions, please contact the development team.

---

## ⚖️ Legal Notice

This platform is for information purposes only. Always consult a qualified lawyer before taking legal action.

---

**Last Updated**: May 29, 2026  
**Version**: 1.0.0  
**Status**: Production Ready
