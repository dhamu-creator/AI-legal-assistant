# ⚡ QUICK REFERENCE GUIDE

**AI Legal Assistant v2.0.0**  
**One-page command reference for developers**

---

## 📋 FOLDER STRUCTURE

```
backend/              ← Node.js API server
  └─ npm run dev      ← Start development server
  └─ npm run seed     ← Populate database

frontend/             ← React web app
  └─ npm run dev      ← Start Vite dev server
  └─ npm run build    ← Build for production

Documentation/
  └─ QUICKSTART.md             ← 5-min setup
  └─ BACKEND_SETUP_GUIDE.md    ← Backend help
  └─ FRONTEND_SETUP_GUIDE.md   ← Frontend help
  └─ DEPLOYMENT_GUIDE.md       ← Go live
  └─ COMPREHENSIVE_TESTING_CHECKLIST.md ← Validation
```

---

## 🚀 QUICK START (Copy-Paste Commands)

### Terminal 1 - Backend

```bash
cd backend
npm install
npm run dev
```

**Expected**: 
```
✅ MongoDB connected successfully
📡 Server running on http://localhost:5000
```

### Terminal 2 - Frontend

```bash
cd frontend
npm install
npm run dev
```

**Expected**: 
```
VITE v5.0.0  ready in XXXms
➜  Local:   http://localhost:3000
```

### Terminal 3 - Seed Database (one time only)

```bash
cd backend
npm run seed
```

**Expected**:
```
✅ Inserted 5 legal documents
✅ Inserted 5 evidence checklists
✅ Database seeding completed successfully!
```

---

## 🔑 CONFIGURATION

### Backend .env

```env
PORT=5000
NODE_ENV=development
MONGO_URI=mongodb://localhost:27017/ai-legal-assistant
GEMINI_API_KEY=your_key_from_makersuite.google.com
PYTHON_BACKEND_URL=http://localhost:8000
```

### Frontend .env

```env
VITE_API_URL=http://localhost:5000/api
```

---

## 🧪 QUICK TESTING

### In Browser Console

```javascript
// Test API connection
fetch('http://localhost:5000/api/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

### cURL Commands

```bash
# Health check
curl http://localhost:5000/api/health

# Get languages
curl http://localhost:5000/api/legal/languages

# Create chat session
curl -X POST http://localhost:5000/api/chat/session \
  -H "Content-Type: application/json" \
  -d '{"userId":"test","language":"en"}'
```

---

## 📱 URLS

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:5000/api |
| Health Check | http://localhost:5000/api/health |
| MongoDB | localhost:27017 |

---

## 📊 API ENDPOINTS (18 Total)

### Chat (5)
```
POST   /api/chat/session
POST   /api/chat/message
GET    /api/chat/history/:id
GET    /api/chat/sessions/:id
DELETE /api/chat/session/:id
```

### FIR (7)
```
POST   /api/fir/create/:id
POST   /api/fir/generate/:id
GET    /api/fir/user/:id
GET    /api/fir/:id
PUT    /api/fir/:id
DELETE /api/fir/:id
POST   /api/fir/evidence/checklist
```

### Legal (4)
```
GET /api/legal/languages
GET /api/legal/crime-categories
GET /api/legal/disclaimer
GET /api/legal/emergency-contacts
```

### Status (2)
```
GET /api/health
GET /api/fir/pdf/:id (planning)
```

---

## 🔧 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| **MongoDB connection refused** | Check `mongod` running: `mongosh` |
| **Port already in use** | Kill process: `lsof -i :5000 \| grep LISTEN \| awk '{print $2}' \| xargs kill -9` |
| **Blank page** | Check DevTools (F12) Console for errors |
| **API 404 errors** | Verify backend running & VITE_API_URL set |
| **GEMINI_API_KEY undefined** | Add to backend/.env & restart |
| **Can't connect to MongoDB** | Check connection string in .env |
| **CORS errors** | Backend must be running on :5000 |

---

## 📚 SUPPORTED LANGUAGES

```
en - English
ta - Tamil (தமிழ்)
hi - Hindi (हिन्दी)
te - Telugu (తెలుగు)
ml - Malayalam (മലയാളം)
ka - Kannada (ಕನ್ನಡ)
```

---

## 🎯 DEVELOPMENT WORKFLOW

```
1. Start Backend       → npm run dev (in backend/)
2. Start Frontend      → npm run dev (in frontend/)
3. Open Browser        → http://localhost:3000
4. Make code changes   → Hot reload automatic
5. Test features       → Use app in browser
6. Check console       → F12 for errors
7. Test APIs          → Use cURL or Postman
```

---

## 🚢 DEPLOYMENT COMMANDS

### Build Frontend

```bash
cd frontend
npm run build
# Creates dist/ folder for deployment
```

### Push to Git

```bash
git add .
git commit -m "Your message"
git push origin main
```

### Deploy Backend

**Railway.app**
```
1. Connect GitHub
2. New Project → Deploy from GitHub
3. Select backend folder
4. Add environment variables
5. Deploy
```

**Render.com**
```
1. New Web Service
2. Connect GitHub
3. Set build/start commands
4. Add environment variables
5. Deploy
```

### Deploy Frontend

**Vercel.com**
```
1. Connect GitHub
2. Import project
3. Set root: frontend
4. Add VITE_API_URL env var
5. Deploy
```

**Netlify.com**
```
1. Connect GitHub
2. Build: npm run build
3. Publish: frontend/dist
4. Add environment variables
5. Deploy
```

---

## 📖 DOCUMENTATION QUICK LINKS

| File | Purpose |
|------|---------|
| QUICKSTART.md | 5-minute setup guide |
| BACKEND_SETUP_GUIDE.md | Backend testing & troubleshooting |
| FRONTEND_SETUP_GUIDE.md | Frontend testing & validation |
| DEPLOYMENT_GUIDE.md | Production deployment |
| COMPREHENSIVE_TESTING_CHECKLIST.md | Full feature validation |
| PROJECT_COMPLETION_REPORT.md | Project status & metrics |
| COMPLETE_DOCUMENTATION.md | Full technical documentation |
| UPGRADE_REPORT.md | What changed in v2.0 |

---

## 🔐 SECURITY CHECKLIST

- [ ] .env file in .gitignore
- [ ] No API keys in source code
- [ ] Environment variables configured on hosting
- [ ] HTTPS enabled (automatic on Vercel/Railway)
- [ ] Rate limiting active (100 req/15min)
- [ ] Input validation working
- [ ] Error messages don't expose system details
- [ ] Database backups configured (Atlas auto-backup)

---

## 📊 PROJECT STATS

| Metric | Value |
|--------|-------|
| Total Files | 42 |
| Lines of Code | 2,880+ |
| Documentation | 2,000+ lines |
| API Endpoints | 18 |
| Database Models | 5 |
| Supported Languages | 6 |
| Crime Categories | 10 |
| Frontend Pages | 4 |

---

## 🎯 FEATURE CHECKLIST

- ✅ AI Chat with crime detection
- ✅ FIR generation (4-step wizard)
- ✅ Emergency help section
- ✅ 6 language support
- ✅ MongoDB database
- ✅ Rate limiting
- ✅ Input validation
- ✅ Error handling
- ✅ Responsive design
- ✅ Production security

---

## 📞 COMMON QUESTIONS

**Q: Where to get Gemini API key?**  
A: makersuite.google.com → Get API Key (free)

**Q: Which database should I use?**  
A: Local MongoDB for dev, MongoDB Atlas for production

**Q: Where to deploy frontend?**  
A: Vercel (recommended) or Netlify

**Q: Where to deploy backend?**  
A: Railway (recommended) or Render or Heroku

**Q: How to run database seed?**  
A: `cd backend && npm run seed` (one time only)

**Q: What if MongoDB not running?**  
A: `mongod` (Windows: download from mongodb.com)

**Q: How to change port?**  
A: Edit backend/.env `PORT=5001`

**Q: How to add more languages?**  
A: Edit frontend/src/i18n/config.js + backend logic

**Q: How to add more crime categories?**  
A: Update models/EvidenceChecklist.js + AIService.js

**Q: How to enable authentication?**  
A: Follow JWT setup in COMPLETE_DOCUMENTATION.md

---

## ⚡ DAILY DEVELOPMENT COMMANDS

```bash
# Start development (backend + frontend)
# Terminal 1
cd backend && npm run dev

# Terminal 2
cd frontend && npm run dev

# Test specific endpoint
curl http://localhost:5000/api/health

# View MongoDB
mongosh

# Build for production
npm run build  # in frontend/

# Deploy to Git
git add . && git commit -m "message" && git push

# Check running processes
lsof -i :5000  # backend
lsof -i :3000  # frontend
lsof -i :27017 # MongoDB
```

---

## 📈 NEXT STEPS

1. ✅ **Day 1**: Setup & test locally (follow QUICKSTART.md)
2. ✅ **Day 2**: Seed database & validate features
3. ✅ **Day 3**: Deploy backend (follow DEPLOYMENT_GUIDE.md)
4. ✅ **Day 4**: Deploy frontend
5. ✅ **Day 5**: Live testing & monitoring
6. ⏭️ **Week 2**: User authentication (JWT)
7. ⏭️ **Week 3**: PDF generation
8. ⏭️ **Month 2**: Advanced features

---

## 🎊 YOU'RE ALL SET!

Your AI Legal Assistant is ready. Follow the commands above to get started.

**Questions?** Check the relevant documentation file listed above.

**Ready to deploy?** Follow DEPLOYMENT_GUIDE.md.

**Let's go live!** 🚀

---

**Version**: 2.0.0  
**Last Updated**: May 29, 2026  
**Status**: 🟢 Production Ready
