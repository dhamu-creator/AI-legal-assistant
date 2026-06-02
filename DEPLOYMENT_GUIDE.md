# 🚀 Deployment Guide - Complete Setup

## 📋 Pre-Deployment Checklist

- [ ] Backend tested locally (npm run dev)
- [ ] Frontend tested locally (npm run dev)
- [ ] MongoDB database running or Atlas cluster created
- [ ] Environment variables configured (.env files)
- [ ] API keys obtained (Gemini API)
- [ ] Database seeded with legal documents
- [ ] All endpoints tested with Postman/cURL
- [ ] No console errors in DevTools
- [ ] No compile errors in terminal

---

## 🗄️ Database Setup

### Option 1: Local MongoDB (Development)

```bash
# Windows - Download Community Edition
# Visit: mongodb.com/try/download/community

# macOS
brew install mongodb-community
brew services start mongodb-community

# Linux
sudo apt-get install mongodb
sudo systemctl start mongodb

# Verify running
mongosh
# Should show: test>
# Type: exit
```

### Option 2: MongoDB Atlas (Production - Recommended)

1. **Create Account**
   - Go to [mongodb.com/cloud](https://mongodb.com/cloud)
   - Sign up (free tier available)

2. **Create Cluster**
   - Click "Create a Deployment"
   - Select Free tier
   - Choose region (e.g., AWS N. Virginia)
   - Click "Create Deployment"

3. **Get Connection String**
   - Go to "Database" → "Connect"
   - Choose "Drivers" → "Node.js"
   - Copy connection string
   - Replace `<password>` with your password
   - Update backend/.env:
     ```env
     MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/ai-legal-assistant
     ```

4. **Add IP Whitelist**
   - Network Access → Add IP Address
   - Allow from anywhere: 0.0.0.0/0

---

## 🌱 Seed Database with Legal Documents

### Run Seed Script

```bash
cd backend
npm run seed
```

Expected output:
```
✅ MongoDB connected successfully
🌱 Starting database seed...
📚 Seeding Legal Documents...
✅ Inserted 5 legal documents
📋 Seeding Evidence Checklists...
✅ Inserted 5 evidence checklists

✅ Database seeding completed successfully!
```

This populates:
- **Legal Documents**: IPC sections, BNS acts, cyber law
- **Evidence Checklists**: Crime-specific evidence requirements
- **Procedures**: Step-by-step legal procedures
- **Emergency Contacts**: Helpline numbers

---

## 🚢 Backend Deployment (Node.js)

### Option 1: Railway (Recommended - Easy)

**Step 1: Setup**
```bash
# Create Railway account at railway.app
# Connect GitHub (GitHub OAuth login)
```

**Step 2: Deploy**
1. Click "New Project"
2. "Deploy from GitHub"
3. Select your repository
4. Select `backend` folder
5. Click "Deploy"

**Step 3: Environment Variables**
1. Go to Variables tab
2. Add each variable from `.env`:
   ```
   PORT=5000
   NODE_ENV=production
   MONGO_URI=your_atlas_connection_string
   GEMINI_API_KEY=your_key
   ```
3. Railway will auto-restart

**Step 4: Get URL**
- Railway provides: `https://your-app.railway.app`
- Backend running! 🎉

---

### Option 2: Render

**Step 1: Setup**
```bash
# Create Render account at render.com
# Connect GitHub
```

**Step 2: New Web Service**
1. Click "New +" → "Web Service"
2. Connect GitHub repository
3. Configure:
   - Name: `ai-legal-assistant-backend`
   - Environment: `Node`
   - Build Command: `npm install`
   - Start Command: `npm start`

**Step 3: Environment Variables**
1. Go to Environment
2. Add all variables from `.env`

**Step 4: Deploy**
- Click "Create Web Service"
- Render will deploy automatically
- URL: `https://your-app.onrender.com`

---

### Option 3: Heroku (Legacy)

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
```

Add environment variables:
```bash
heroku config:set GEMINI_API_KEY=your_key
```

---

## 🎨 Frontend Deployment

### Option 1: Vercel (Recommended - Best for React)

**Step 1: Setup**
```bash
# Create Vercel account at vercel.com
# Connect GitHub
```

**Step 2: Import Project**
1. Click "Add New..." → "Project"
2. "Import Git Repository"
3. Select your repository

**Step 3: Configure**
1. Framework: Vite
2. Root Directory: `frontend`
3. Build Command: `npm run build`
4. Output Directory: `dist`

**Step 4: Environment Variables**
```
VITE_API_URL=https://your-backend.railway.app/api
```

**Step 5: Deploy**
- Click "Deploy"
- Vercel auto-deploys on every git push
- URL: `https://your-app.vercel.app`

---

### Option 2: Netlify

**Step 1: Connect GitHub**
```bash
# Go to netlify.com
# Click "Add new site" → "Import an existing project"
# Connect GitHub
```

**Step 2: Configure**
1. Repository: Select your repo
2. Branch: `main`
3. Build command: `cd frontend && npm run build`
4. Publish directory: `frontend/dist`

**Step 3: Environment Variables**
```
VITE_API_URL=https://your-backend.railway.app/api
```

**Step 4: Deploy**
- Netlify auto-deploys
- Get URL: `https://your-app.netlify.app`

---

## 🔗 Connect Frontend to Backend

### Update API Base URL

**frontend/.env.production**
```env
VITE_API_URL=https://your-backend-url.com/api
```

Example (if using Railway):
```env
VITE_API_URL=https://ai-legal-backend.railway.app/api
```

### Build for Production

```bash
cd frontend
npm run build
```

Creates `dist/` folder with optimized files.

---

## ✅ Post-Deployment Testing

### Test 1: Backend Health Check

```bash
curl https://your-backend.railway.app/api/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-29T10:00:00Z",
  "uptime": 12345
}
```

### Test 2: Frontend Load

1. Visit: `https://your-app.vercel.app`
2. Should load Home page
3. Check Network tab (DevTools)
4. No CORS errors

### Test 3: Chat API Call

1. Go to Chatbot page
2. Send test message
3. Check DevTools → Network
4. Should see API call to backend
5. Get response in 5-10 seconds

### Test 4: FIR Generation

1. Go to FIR Generator
2. Fill form completely
3. Click "Generate"
4. Should produce FIR draft
5. Download should work

---

## 🔒 Security Setup

### Step 1: Enable HTTPS

**Railway/Render**: Automatic ✅

**Vercel/Netlify**: Automatic ✅

### Step 2: Set Production Environment

**backend/.env**
```env
NODE_ENV=production
```

### Step 3: Update CORS

**backend/server.js**
```javascript
app.use(cors({
  origin: 'https://your-app.vercel.app',
  credentials: true
}));
```

### Step 4: API Rate Limiting

Already configured in backend:
```javascript
// 100 requests per 15 minutes for chat
const chatLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});
```

---

## 📊 Monitoring & Logs

### Railway Logs
1. Dashboard → Your project
2. "Deployments" → Select deployment
3. "Logs" tab shows real-time logs

### Vercel Logs
1. Dashboard → Your project
2. "Deployments" → Select deployment
3. "Build Logs" or "Function Logs"

### Monitor Errors
- Set up error tracking with:
  - Sentry (sentry.io)
  - LogRocket (logrocket.com)
  - Datadog (datadoghq.com)

---

## 🔄 Continuous Deployment

### Auto-Deploy on Git Push

**Railway/Render/Vercel**: Automatic on main branch push ✅

### Manual Redeployment

**Railway**
```
Dashboard → Deployments → "Redeploy" button
```

**Render**
```
Dashboard → Manual Deploy → "Deploy latest commit"
```

**Vercel**
```
Dashboard → Deployments → "Redeploy" next to latest
```

---

## 💾 Database Backups

### MongoDB Atlas Auto-Backup

1. Go to "Backup" in Atlas
2. Daily automated backups (14-day retention)
3. Manual backups available anytime

### Export Database

```bash
# Backup to file
mongodump --uri="mongodb+srv://user:pass@cluster..." \
          --out=./backup

# Restore from backup
mongorestore --uri="mongodb+srv://user:pass@cluster..." \
             ./backup
```

---

## 🚨 Troubleshooting Deployment

### Problem: Backend won't start

**Check logs:**
```bash
# Railway: View Logs tab
# Render: Check Logs
```

**Common causes:**
- Missing environment variables
- Database connection error
- Port in use
- Invalid API key

### Problem: Frontend shows blank page

**Check:**
1. Network tab for 404 errors
2. Console for JavaScript errors
3. VITE_API_URL environment variable set
4. Backend API running and accessible

### Problem: API calls return 404

**Causes:**
- Backend not running
- Wrong API URL in frontend
- Endpoint doesn't exist
- Route not mounted

**Fix:**
```bash
# Verify backend running
curl https://your-backend/api/health

# Check frontend VITE_API_URL
# In browser console: console.log(import.meta.env.VITE_API_URL)
```

### Problem: Database connection timeout

**Solution:**
1. MongoDB Atlas: Add IP to whitelist
2. Check connection string
3. Verify MONGO_URI in environment variables
4. Test connection with MongoDB Compass

---

## 📈 Scaling for Production

### When you need more power:

**Backend:**
- Railway: Upgrade to paid tier
- Render: Select larger instance
- Heroku: Use Professional tier

**Database:**
- MongoDB Atlas: Upgrade cluster tier
- Enable auto-scaling if needed

**Frontend:**
- Vercel/Netlify: Included in free tier
- Add CDN for images/media

---

## 🎯 Final Checklist

- [ ] Backend deployed and running
- [ ] Frontend deployed and running
- [ ] Database connected and seeded
- [ ] Environment variables set
- [ ] HTTPS working (automatic)
- [ ] API endpoints tested
- [ ] Chat functionality working
- [ ] FIR generation working
- [ ] All languages working
- [ ] Mobile responsive tested
- [ ] Monitoring set up (optional)
- [ ] Backups configured

---

## 📞 Production URLs (Example)

```
Frontend: https://ai-legal-assistant.vercel.app
Backend:  https://ai-legal-backend.railway.app
Database: MongoDB Atlas cluster
```

**Your application is live!** 🎉

---

## 🔐 Important Security Notes

1. **Never commit .env files** - Use .env.example
2. **Rotate API keys** regularly
3. **Monitor usage** - Check API logs
4. **Enable logging** - Track all requests
5. **Backup database** - Daily automated backups
6. **Update dependencies** - Keep packages current

---

**Deployment completed successfully!**

Next: Monitor performance and gather user feedback.
