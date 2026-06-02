# 🎨 Frontend Setup & Testing Guide

## ⚡ Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

This installs:
- ✅ React 18 + Vite (fast development)
- ✅ React Router (page navigation)
- ✅ Tailwind CSS (styling)
- ✅ Framer Motion (animations)
- ✅ i18next (6 languages)
- ✅ Axios (API calls)
- ✅ Heroicons (icons)

### Step 2: Start Development Server

```bash
npm run dev
```

Expected output:
```
  VITE v5.0.0  ready in 123 ms

  ➜  Local:   http://localhost:3000
  ➜  press h to show help
```

### Step 3: Open in Browser

Visit: **http://localhost:3000**

You should see:
- 🏠 Home page with features
- 📱 Mobile responsive design
- ⚡ Smooth animations
- 🌍 6 language options

---

## 🧪 Testing All Features

### Test 1: Home Page

✅ **What to test:**
- Hero section displays correctly
- Feature cards are visible
- Call-to-action buttons work
- Responsive layout on mobile/tablet/desktop
- Legal disclaimer visible

**How:**
1. Navigate to http://localhost:3000
2. Scroll through entire page
3. Click "Get Started" button → Should go to Chatbot
4. Test responsive: F12 → Responsive Design Mode → Toggle sizes

---

### Test 2: Chatbot Page

✅ **Prerequisites:**
- Backend running on http://localhost:5000
- GEMINI_API_KEY configured in backend/.env

✅ **What to test:**
1. Language selector (top right)
   - Click dropdown
   - Select different languages
   - Verify UI updates

2. Chat interface
   - Type message: "What should I do if someone steals my phone?"
   - Click Send button
   - Wait for AI response (5-10 seconds first time)
   - Response should include crime category badge
   - Message appears in chat history

3. Auto-scroll
   - Send multiple messages
   - Chat should auto-scroll to latest

4. Loading indicator
   - While waiting for response, animated loader appears
   - Disappears when response arrives

5. Empty state
   - Refresh page
   - Should see welcome message with example questions

**Test Messages (Different Crime Types):**
- "Someone is blackmailing me with intimate photos" → Blackmail
- "My online shopping account was hacked" → Cyber Fraud
- "My wife hits me when angry" → Domestic Violence
- "A stranger in a car took my bag" → Robbery
- "My neighbor is constantly harassing me" → Harassment

---

### Test 3: FIR Generator

✅ **What to test:**

**Step 1: Incident Details**
- Type title: "Mobile Phone Theft"
- Select crime category: "Theft"
- Write incident details: "My phone was stolen from XYZ cafe"
- Pick date and location
- Click "Next" → Should go to Step 2

**Step 2: Your Information**
- Enter name, phone, email
- Type address
- Click "Next" → Should go to Step 3

**Step 3: Additional Details**
- Enter suspect name (optional)
- Describe suspect
- List evidence items (one per line):
  ```
  Phone Model: iPhone 13
  IMEI: 123456789
  Phone Cover Color: Black
  Screen Protector: Yes
  ```
- Click "Generate" → Should show Step 4

**Step 4: Preview**
- Review FIR draft text
- Should show:
  - Your details
  - Incident information
  - Crime category
  - IPC sections
  - Professional formatting
- Click "Download" → .txt file should download
- Click "Create New" → Should reset form

✅ **Validation:**
- Language selector works
- All form fields accept input
- Form validation (required fields)
- FIR draft generation works
- Download functionality works

---

### Test 4: Emergency Help

✅ **What to test:**

1. Emergency Contacts
   - See 5 contact cards:
     - 🚓 Police 100
     - 👩 Women 1091
     - 🔒 Cyber 1930
     - 👶 Childline 1098
     - 🚑 Emergency 112
   - Contacts display correct numbers
   - Description visible

2. Legal Procedures
   - See 3 collapsible sections:
     - "If Police Refuse to File FIR"
     - "Steps to File Police Complaint"
     - "Cybercrime Reporting"
   - Each has 5+ numbered steps
   - Steps are clear and actionable

3. Important Notes
   - 6 legal notes displayed
   - Blue background styling
   - All text readable

---

## 🌍 Test Multilingual Support

### Test Language Switching

1. **Go to Chatbot page**
2. **Click language dropdown (top right)**
3. **Select each language:**
   - 🇮🇳 English (en)
   - 🇮🇳 Tamil (ta)
   - 🇮🇳 Hindi (hi)
   - 🇮🇳 Telugu (te)
   - 🇮🇳 Malayalam (ml)
   - 🇮🇳 Kannada (ka)
4. **Verify for each:**
   - UI text updates
   - Language label shows
   - API calls include correct language code
   - Responses translated to that language

### Test Messages in Different Languages

**English:**
```
What should I do if someone steals my phone?
```

**Hindi:**
```
अगर कोई मेरा फोन चुरा ले तो मुझे क्या करना चाहिए?
```

**Tamil:**
```
ஒருவர் என் தொலைபேசியை திருடிக்கொண்டால் நான் என்ன செய்ய வேண்டும்?
```

---

## 🔗 API Integration Testing

### Check Network Requests

1. **Open DevTools**: F12
2. **Go to Network tab**
3. **Send a chat message**
4. **Look for requests:**
   - `POST /api/chat/session` (first time only)
   - `POST /api/chat/message` (on send)
   - Check response status: 200 OK
   - Check response body has AI message

### Check Console

1. **Open DevTools**: F12
2. **Go to Console tab**
3. **Send messages**
4. **No red errors should appear**
5. **Check for warnings** (should be minimal)

---

## 📱 Responsive Design Testing

### Desktop
- Width: 1920px
- Test at http://localhost:3000
- All content fits
- Sidebar layouts work

### Tablet
- F12 → Responsive Design Mode
- Size: iPad (768x1024)
- Buttons accessible
- Text readable
- No overflow

### Mobile
- F12 → Responsive Design Mode
- Size: iPhone 12 (390x844)
- Single column layout
- Touch targets 48px minimum
- Scrolling smooth
- No horizontal overflow

---

## ⚡ Performance Testing

### Build Optimization

```bash
npm run build
```

Should produce:
- dist/ folder (< 500KB gzipped)
- index.html (small)
- js chunks (code split)
- css optimized (Tailwind)

### Load Time

With `npm run dev`:
- First load: < 2 seconds
- HMR (Hot reload): < 500ms
- API response: 1-5 seconds (depending on AI)

---

## 🎨 UI/UX Testing

### Animations
- ✅ Page transitions smooth
- ✅ Buttons have hover effects
- ✅ Messages fade in
- ✅ Loading spinner animated
- ✅ No jank or stuttering

### Colors & Contrast
- ✅ Text readable on all backgrounds
- ✅ Buttons clearly clickable
- ✅ Error messages visible
- ✅ Success states obvious

### Accessibility
- ✅ Tab navigation works
- ✅ Can tab through all buttons
- ✅ Focus indicators visible
- ✅ Screen reader friendly (bonus)

---

## 🐛 Common Issues & Fixes

### Problem: "Cannot GET /api/chat/session"

**Cause:** Backend not running  
**Fix:**
```bash
# Terminal 1: Start backend
cd backend
npm run dev

# Terminal 2: Start frontend
cd frontend
npm run dev
```

### Problem: Chatbot shows spinner forever

**Cause:** GEMINI_API_KEY missing or invalid  
**Fix:**
1. Get key from makersuite.google.com
2. Add to backend/.env
3. Restart backend with `npm run dev`

### Problem: Language selector not working

**Cause:** i18next not configured properly  
**Fix:**
1. Check frontend/src/i18n/config.js exists
2. Verify language files loaded
3. Clear browser cache: Ctrl+Shift+Delete
4. Refresh page

### Problem: Styles not applying (no colors)

**Cause:** Tailwind CSS not building  
**Fix:**
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### Problem: Form not submitting

**Cause:** Validation failing silently  
**Fix:**
1. Open DevTools → Console
2. Look for error messages
3. Check all required fields filled
4. Verify format matches expectations

---

## 🔄 Testing Full Flow

### End-to-End Test (10 minutes)

1. **Start servers**
   ```bash
   # Terminal 1
   cd backend && npm run dev
   
   # Terminal 2
   cd frontend && npm run dev
   ```

2. **Test Home Page**
   - View features
   - Click "Get Started"

3. **Test Chatbot**
   - Create session
   - Send message
   - Get response
   - View crime category

4. **Test FIR Generator**
   - Fill form (all fields)
   - Generate FIR
   - Review draft
   - Download file

5. **Test Emergency Help**
   - View contacts
   - Read procedures
   - Check formatting

6. **Test Language Switching**
   - Change language
   - Send message in Tamil/Hindi
   - Verify translation

✅ **If all tests pass**: Frontend working perfectly!

---

## 🚀 Building for Production

```bash
cd frontend
npm run build
```

This creates:
- `dist/` folder (ready to deploy)
- Optimized JavaScript
- Minified CSS
- Compressed images

Deploy `dist/` folder to:
- **Vercel** (recommended)
- **Netlify**
- **GitHub Pages**
- **Your own server**

---

## 📊 Checklist

- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] Home page loads
- [ ] Chatbot sends/receives messages
- [ ] FIR generator works
- [ ] Emergency help displays
- [ ] Language switching works
- [ ] Mobile responsive
- [ ] No console errors
- [ ] Ready for production

---

## 📞 Support

- **Blank page?** Check console (F12)
- **API errors?** Verify backend running
- **Styles broken?** Clear cache + reinstall
- **Can't send message?** Check GEMINI_API_KEY

---

**Status**: 🟢 Ready to Test
