# 🚀 Backend Setup & Testing Guide

## ⚡ Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
cd backend
npm install
```

This installs:
- ✅ Express.js (web framework)
- ✅ Mongoose (MongoDB driver)
- ✅ Google Generative AI (Gemini API)
- ✅ CORS, Helmet, Morgan (security & logging)
- ✅ Nodemon (development auto-reload)

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Server
PORT=5000
NODE_ENV=development

# Database
MONGO_URI=mongodb://localhost:27017/ai-legal-assistant

# API Keys (get free from below)
GEMINI_API_KEY=your_key_here

# Other optional keys
OPENAI_API_KEY=optional
GROQ_API_KEY=optional

# Python RAG Backend (optional)
PYTHON_BACKEND_URL=http://localhost:8000
```

### Step 3: Get API Keys

#### Option A: Gemini API (Recommended - Free)
1. Go to [makersuite.google.com](https://makersuite.google.com)
2. Click "Get API Key"
3. Create new API key
4. Copy and paste into `.env` as `GEMINI_API_KEY`

#### Option B: Alternative LLM Providers
- **OpenAI**: openai.com/api/
- **Groq**: groq.com/openrouter

### Step 4: Setup MongoDB

**Option A: Local MongoDB (Recommended for development)**

```bash
# Windows - Download from mongodb.com/try/download/community
# Run: mongod

# macOS
brew install mongodb-community
brew services start mongodb-community

# Linux
sudo apt-get install mongodb
sudo systemctl start mongodb
```

**Option B: MongoDB Atlas (Cloud)**

1. Go to [mongodb.com/cloud](https://mongodb.com/cloud)
2. Create free account
3. Create cluster
4. Get connection string
5. Add to `.env` as `MONGO_URI`

Example: `mongodb+srv://user:pass@cluster.mongodb.net/ai-legal-assistant`

### Step 5: Start Backend Server

```bash
npm run dev
```

Expected output:
```
✅ MongoDB connected successfully
📡 Server running on http://localhost:5000
🔗 API Base: http://localhost:5000/api
```

---

## 🧪 Testing the API

### Test 1: Health Check

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-29T10:00:00Z",
  "uptime": 123.45
}
```

### Test 2: Create Chat Session

```bash
curl -X POST http://localhost:5000/api/chat/session \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "test-user-123",
    "language": "en"
  }'
```

Expected response:
```json
{
  "success": true,
  "data": {
    "_id": "session-id",
    "userId": "test-user-123",
    "language": "en",
    "messages": [],
    "createdAt": "2026-05-29T10:00:00Z"
  }
}
```

### Test 3: Send Chat Message

```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "session-id-from-test-2",
    "message": "What should I do if someone steals my mobile phone?",
    "language": "en"
  }'
```

Expected response includes:
```json
{
  "success": true,
  "data": {
    "userMessage": "What should I do if someone steals my mobile phone?",
    "aiResponse": "If your mobile phone has been stolen, here are the steps...",
    "detectedCrimeCategory": "Theft",
    "relevantIPCSection": "IPC 379",
    "language": "en"
  }
}
```

### Test 4: Get Legal Languages

```bash
curl http://localhost:5000/api/legal/languages
```

Expected response:
```json
{
  "success": true,
  "data": [
    {"code": "en", "name": "English"},
    {"code": "ta", "name": "Tamil"},
    {"code": "hi", "name": "Hindi"},
    {"code": "te", "name": "Telugu"},
    {"code": "ml", "name": "Malayalam"},
    {"code": "ka", "name": "Kannada"}
  ]
}
```

### Test 5: Get Crime Categories

```bash
curl http://localhost:5000/api/legal/crime-categories
```

Expected response:
```json
{
  "success": true,
  "data": [
    "Theft",
    "Robbery",
    "Cyber Fraud",
    "Harassment",
    "Domestic Violence",
    "Blackmail",
    "Online Scams",
    "Identity Theft",
    "Financial Fraud",
    "Physical Assault"
  ]
}
```

### Test 6: Generate FIR Report

```bash
curl -X POST http://localhost:5000/api/fir/generate/test-user-123 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mobile Phone Theft",
    "incidentDetails": "My phone was stolen from a coffee shop in Delhi on 2026-05-29",
    "incidentDate": "2026-05-29",
    "incidentLocation": "Coffee Shop, Connaught Place, Delhi",
    "crimeCategory": "Theft",
    "complainantDetails": {
      "name": "John Doe",
      "phone": "9876543210",
      "email": "john@example.com",
      "address": "Delhi, India"
    },
    "language": "en"
  }'
```

Expected response includes FIR draft text.

---

## 🛠️ Troubleshooting

### Problem: "MongoDB connection refused"

**Solution:**
```bash
# Check if MongoDB is running
# Windows: Open MongoDB Compass or check Services
# macOS: brew services list
# Linux: sudo systemctl status mongodb

# If not running:
# Windows: Download from mongodb.com
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongodb
```

### Problem: "GEMINI_API_KEY is undefined"

**Solution:**
1. Get free API key from makersuite.google.com
2. Add to backend/.env:
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```
3. Restart server with `npm run dev`

### Problem: "Cannot find module '@google/generative-ai'"

**Solution:**
```bash
cd backend
npm install @google/generative-ai
```

### Problem: "Port 5000 already in use"

**Solution:**
```bash
# Change port in .env
PORT=5001

# Or kill process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Problem: "CORS error from frontend"

**Solution:**
Ensure backend `.env` has:
```env
CORS_ORIGIN=http://localhost:3000
```

And restart server.

---

## 📊 All API Endpoints (18)

### Chat Endpoints (5)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/chat/session` | Create new chat session |
| POST | `/api/chat/message` | Send message & get response |
| GET | `/api/chat/history/:id` | Get chat history |
| GET | `/api/chat/sessions/:id` | Get all user sessions |
| DELETE | `/api/chat/session/:id` | Delete session |

### FIR Endpoints (7)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/fir/create/:id` | Create FIR report |
| POST | `/api/fir/generate/:id` | Generate FIR draft |
| GET | `/api/fir/user/:id` | Get user's FIRs |
| GET | `/api/fir/:id` | Get specific FIR |
| PUT | `/api/fir/:id` | Update FIR |
| DELETE | `/api/fir/:id` | Delete FIR |
| POST | `/api/fir/evidence/checklist` | Get evidence list |

### Legal Endpoints (4)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/legal/languages` | Get supported languages |
| GET | `/api/legal/crime-categories` | Get crime types |
| GET | `/api/legal/disclaimer` | Get legal disclaimer |
| GET | `/api/legal/emergency-contacts` | Get emergency numbers |

---

## 📱 Testing with Postman

1. Download Postman from [postman.com](https://postman.com)
2. Import collection:
   - File → New → HTTP Request
   - Set method: POST
   - URL: `http://localhost:5000/api/chat/session`
   - Headers: `Content-Type: application/json`
   - Body:
     ```json
     {
       "userId": "test-user",
       "language": "en"
     }
     ```
   - Click Send

---

## 🔍 Backend Architecture

```
Backend Server (Express.js)
    ↓
Middleware Stack:
    ├─ Express JSON Parser
    ├─ CORS Handler
    ├─ Helmet Security
    ├─ Morgan Logging
    └─ Rate Limiter
    ↓
Routes (3 files):
    ├─ Chat Routes (5 endpoints)
    ├─ FIR Routes (7 endpoints)
    └─ Legal Routes (4 endpoints)
    ↓
Controllers (2 files):
    ├─ ChatController
    └─ FIRController
    ↓
Services (4 files):
    ├─ AIService (Gemini integration)
    ├─ ChatService (conversation logic)
    ├─ FIRService (FIR generation)
    └─ LanguageDetectionService
    ↓
Database:
    ├─ MongoDB (local/Atlas)
    └─ Models (5 schemas)
```

---

## 🚀 Next Steps

1. ✅ Install & start backend
2. ✅ Test API endpoints
3. ⏭️ Test frontend integration
4. ⏭️ Deploy to production
5. ⏭️ Setup authentication

---

## 📞 Support

- **Port Issues?** See Troubleshooting section
- **API Key Issues?** Check makersuite.google.com
- **Database Issues?** Verify MongoDB is running
- **Still stuck?** Check logs in terminal

---

**Status**: 🟢 Ready to Test
