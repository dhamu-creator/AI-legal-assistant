# 🚀 Quick Start Guide - AI Legal Assistant

## 5-Minute Setup

### Step 1: Start MongoDB

If using local MongoDB:
```bash
mongod
```

Or use MongoDB Atlas (cloud) - get connection string from https://www.mongodb.com/cloud/atlas

---

### Step 2: Start Backend

**Terminal 1:**
```bash
cd backend

# Install dependencies (first time only)
npm install

# Create .env file
copy .env.example .env

# Edit .env and add your Gemini API key:
# GEMINI_API_KEY=your_key_from_makersuite.google.com

# Start server
npm run dev
```

Expected output:
```
╔═══════════════════════════════════════════════════════╗
║   🏛️  AI LEGAL ASSISTANT - Backend Server              ║
║   Status: 🟢 Running                                   ║
║   Port: 5000                                           ║
║   Environment: development                            ║
║   Database: MongoDB Connected                         ║
╚═══════════════════════════════════════════════════════╝
```

---

### Step 3: Start Frontend

**Terminal 2:**
```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

Expected output:
```
  VITE v5.0.0  ready in X ms

  ➜  Local:   http://localhost:3000/
  ➜  press h + enter to show help
```

---

### Step 4: Open in Browser

Visit: **http://localhost:3000**

You should see the AI Legal Assistant homepage! 🎉

---

## 🎯 Quick Test

### Test 1: Chat with AI
1. Click "Chatbot" in navigation
2. Select language (English, Tamil, Hindi, etc.)
3. Type: "My phone was stolen in a bus stand"
4. Click Send
5. See AI response with crime category and legal sections!

### Test 2: Generate FIR
1. Click "FIR Generator"
2. Fill in the form step by step
3. Click "Generate FIR"
4. See professional FIR draft
5. Download as text

### Test 3: Emergency Help
1. Click "Emergency Help"
2. See emergency contact numbers
3. See step-by-step legal procedures

---

## 📝 Environment Configuration

### Backend (.env file)

```env
# Server
PORT=5000
NODE_ENV=development

# Database
MONGO_URI=mongodb://localhost:27017/ai-legal-assistant

# AI API
GEMINI_API_KEY=your_api_key_here

# Other settings
JWT_SECRET=your_secret_key
CORS_ORIGIN=http://localhost:3000
```

### Get Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Paste in backend/.env

---

## 🔧 Troubleshooting

### Problem: Port 5000 in use
```bash
# PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess
Stop-Process -Name node -Force
```

### Problem: MongoDB connection error
```bash
# Check if MongoDB is running
mongod --version

# Start MongoDB if not running
mongod
```

### Problem: Gemini API key not working
1. Check you got key from: https://makersuite.google.com/app/apikey
2. Verify it's correctly pasted in .env
3. Restart backend: `npm run dev`

### Problem: Frontend won't load
1. Check backend is running (http://localhost:5000/api/health)
2. Clear browser cache (Ctrl+Shift+Delete)
3. Restart frontend: Ctrl+C then `npm run dev`

---

## 📱 Testing the API

### Test Chat Endpoint

Using PowerShell:

```powershell
# Create session
$session = Invoke-WebRequest -Uri "http://localhost:5000/api/chat/session" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"userId":"test-user","language":"en"}' | ConvertFrom-Json

# Send message
$sessionId = $session.data._id
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/chat/message" `
  -Method POST `
  -ContentType "application/json" `
  -Body "{`"sessionId`":`"$sessionId`",`"message`":`"My phone was stolen`",`"language`":`"en`"}"

$response.Content | ConvertFrom-Json
```

---

## 📊 Supported Features

### ✅ Working Now
- Chat interface with AI
- Crime category detection
- FIR generation
- Multilingual support (6 languages)
- Emergency contacts
- Legal procedures
- Rate limiting
- Input validation

### 🔄 Coming Soon
- User authentication
- PDF download
- Voice input/output
- Lawyer recommendations
- Legal document library
- Payment integration

---

## 📂 Project Structure Quick Reference

```
backend/
  ├── server.js           ← Start here
  ├── .env                ← Your config
  ├── models/             ← Database schemas
  ├── controllers/        ← Business logic
  ├── routes/             ← API endpoints
  └── services/           ← AI integration

frontend/
  ├── src/
  │   ├── App.jsx         ← Main app
  │   ├── pages/          ← Web pages
  │   ├── services/       ← API client
  │   └── i18n/           ← Languages
  └── vite.config.js      ← Build config
```

---

## 🌐 Supported Languages

| Code | Language | Native |
|------|----------|--------|
| en | English | English |
| ta | Tamil | தமிழ் |
| hi | Hindi | हिन्दी |
| te | Telugu | తెలుగు |
| ml | Malayalam | മലയാളം |
| ka | Kannada | ಕನ್ನಡ |

---

## 🔗 Important Links

- **Gemini API Key**: https://makersuite.google.com/app/apikey
- **MongoDB Atlas**: https://www.mongodb.com/cloud/atlas
- **Frontend Docs**: frontend/README.md
- **Backend Docs**: backend/README.md
- **Full Documentation**: COMPLETE_DOCUMENTATION.md

---

## ✅ Success Checklist

- [ ] MongoDB running
- [ ] Backend started on port 5000
- [ ] Frontend started on port 3000
- [ ] Can access http://localhost:3000
- [ ] Can send a chat message
- [ ] Can generate a FIR
- [ ] Can see emergency contacts

---

## 🎓 Learning Path

1. **Understand the Flow**
   - User sends message → Frontend
   - Frontend calls API → Backend
   - Backend processes with AI → Gemini API
   - Response back to Frontend
   - Display in UI

2. **Explore the Code**
   - Backend: models/ → controllers/ → routes/
   - Frontend: pages/ → services/ → components/

3. **Customize**
   - Add new legal sections to models
   - Modify FIR template in services
   - Update UI in pages/

---

## 🚀 Next Steps

### Development
```bash
cd backend && npm run dev    # Terminal 1
cd frontend && npm run dev   # Terminal 2
```

### Production Build
```bash
# Frontend
cd frontend
npm run build
npm run preview

# Backend
cd backend
npm start
```

### Deploy
- Frontend: Vercel.com
- Backend: Railway.app or Render.com
- Database: MongoDB Atlas

---

## 📞 Need Help?

1. Check **COMPLETE_DOCUMENTATION.md** for detailed info
2. Check **troubleshooting** section above
3. Check backend/models/ for database structure
4. Check frontend/src/services/api.js for API client

---

**You're all set! 🎉 Start building amazing legal guidance experiences!**
