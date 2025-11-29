# 🚀 FINAL DEPLOYMENT GUIDE
## Railway + Vercel + Supabase

**Total Time:** 20 minutes  
**Total Cost:** $5/month

---

## ✅ **STEP 1: SUPABASE DATABASE (5 min)**

### 1.1 Create Project
1. Go to [supabase.com](https://supabase.com)
2. Click "New Project"
3. **Name:** `jobika`
4. **Password:** `23110081aiiTgn` (SAVED)
5. **Region:** Mumbai (South Asia)
6. Click "Create"
7. Wait 2-3 minutes

### 1.2 Check Project Status
- If project shows "PAUSED" → Click "Restore"
- Wait until status is "ACTIVE"

### 1.3 Get Connection String
1. Settings → Database
2. Find "Connection Pooling" section
3. Copy the **Transaction** mode URI:
```
postgresql://postgres.eabkwiklxjbqbfxcdlkk:23110081aiiTgn@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

### 1.4 Run Database Schema
1. SQL Editor → New Query
2. Copy contents of `backend/database/postgres_schema.sql`
3. Paste and click "Run"
4. Should see "Success. No rows returned"

---

## ✅ **STEP 2: RAILWAY BACKEND (10 min)**

### 2.1 Install Railway CLI
```bash
curl -fsSL https://railway.app/install.sh | sh
```

### 2.2 Login
```bash
railway login
```

### 2.3 Initialize Project
```bash
cd /Users/roshwinram/Downloads/JoBika_Pyt
railway init
# Name: jobika-backend
```

### 2.4 Set Environment Variables
```bash
railway variables set DATABASE_TYPE=postgres
railway variables set DATABASE_URL="postgresql://postgres.eabkwiklxjbqbfxcdlkk:23110081aiiTgn@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
railway variables set GEMINI_API_KEY="AIzaSyCfUUpFaa5GQ3F45znzykDS-eZNOimfhdg"
railway variables set JWT_SECRET="jobika-production-secret-key-2024"
railway variables set NODE_ENV=production
railway variables set DATABASE_SSL=true
```

### 2.5 Deploy
```bash
cd backend
railway up
```

### 2.6 Get Your Backend URL
```bash
railway domain
# Example: jobika-backend-production.up.railway.app
```

**SAVE THIS URL!** You'll need it for frontend.

---

## ✅ **STEP 3: VERCEL FRONTEND (5 min)**

### 3.1 Update API URL
Edit `app/assets/js/api.js`:
```javascript
// Change this line:
const API_URL = 'http://localhost:3000';

// To your Railway URL:
const API_URL = 'https://jobika-backend-production.up.railway.app';
```

### 3.2 Commit Changes
```bash
git add app/assets/js/api.js
git commit -m "Update API URL for production"
git push origin master
```

### 3.3 Deploy to Vercel
**Vercel is already linked to your GitHub!**

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Find your project: `prj_cBYpfrWqhTiJAiI3KlVD6cSINqaG`
3. It should auto-deploy from GitHub push
4. Or click "Deploy" manually

**Your frontend URL:** `https://jobika.vercel.app`


---

## ✅ **STEP 4: UPDATE CORS (2 min)**

### 4.1 Add Frontend URL to Backend
```bash
railway variables set ALLOWED_ORIGINS="https://jobika.vercel.app"
```

### 4.2 Redeploy Backend
```bash
cd backend
railway up
```

---

## ✅ **STEP 5: TEST EVERYTHING (3 min)**

### 5.1 Test Backend
```bash
curl https://your-railway-url.railway.app/health
# Should return: {"status":"ok","database":"connected"}
```

### 5.2 Test Frontend
1. Open `https://jobika.vercel.app`
2. Click "Register"
3. Create account
4. Upload resume
5. Chat with Orion AI
6. Search jobs
7. Check dashboard

---

## 🎉 **YOU'RE LIVE!**

```
✅ Frontend: https://jobika.vercel.app
✅ Backend: https://your-url.railway.app
✅ Database: Supabase (Mumbai)
✅ AI: Gemini (FREE tier)
```

**Cost:** $5/month (Railway only)

---

## 🔧 **TROUBLESHOOTING**

### Backend won't start
```bash
# Check logs
railway logs

# Common fixes:
# 1. Verify DATABASE_URL is correct
# 2. Check GEMINI_API_KEY is valid
# 3. Ensure all env vars are set
```

### Frontend can't connect to backend
```bash
# 1. Check API_URL in app/assets/js/api.js
# 2. Verify CORS is set: railway variables
# 3. Check Railway backend is running
```

### Database connection fails
```bash
# 1. Check Supabase project is ACTIVE (not paused)
# 2. Use Connection Pooling URI (port 6543)
# 3. Verify password is correct
```

---

## 📊 **NEXT STEPS**

### Week 1: Polish
- [ ] Test all features
- [ ] Fix any bugs
- [ ] Improve UI/UX
- [ ] Add loading states

### Week 2: Add Features
- [ ] Email notifications (Resend)
- [ ] Payment integration (Razorpay)
- [ ] Job alerts
- [ ] Referral system

### Week 3: Launch
- [ ] Product Hunt
- [ ] Twitter/LinkedIn
- [ ] Reddit communities
- [ ] Email beta list

### Week 4: Growth
- [ ] SEO optimization
- [ ] Content marketing
- [ ] Social media
- [ ] Partnerships

---

**Ready to deploy? Start with Step 1! 🚀**
