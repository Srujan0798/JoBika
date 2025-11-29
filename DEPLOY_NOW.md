# JoBika - Production Deployment Guide

## 🎯 DEPLOY WHAT'S READY TODAY

### Current Stack (Production-Ready)
- **Backend:** Node.js + Express
- **Frontend:** Vanilla JavaScript
- **Database:** SQLite (dev) → PostgreSQL (production)
- **AI:** Google Gemini (FREE)
- **Auth:** JWT + bcrypt

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### 1. Environment Variables
```bash
# Required for production
GEMINI_API_KEY=your_key_here
DATABASE_TYPE=postgres
DATABASE_URL=postgresql://user:pass@host:5432/jobika
JWT_SECRET=generate_strong_secret_key
NODE_ENV=production
ALLOWED_ORIGINS=https://yourdomain.com
```

### 2. Database Migration (SQLite → PostgreSQL)

**Current schema is simple - easy migration:**
```sql
-- Already have these tables:
- users
- applications  
- jobs
- resumes
- chat_history

-- Migration script:
node backend/database/migrate-to-postgres.js
```

### 3. Deploy Backend (Railway/Render)

**Option A: Railway**
1. Connect GitHub repo
2. Set environment variables
3. Deploy command: `cd backend && node server.js`
4. Auto-deploys on push

**Option B: Render**
1. New Web Service
2. Build: `cd backend && npm install`
3. Start: `node server.js`
4. Environment variables in dashboard

### 4. Deploy Frontend (Vercel)

```bash
vercel deploy --prod
```

**Important:** Update API URL in frontend:
```javascript
// app/assets/js/api.js
const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-backend.railway.app'
  : 'http://localhost:3000';
```

---

## 🚀 DEPLOYMENT STEPS

### Step 1: Test Locally
```bash
# 1. Start backend
cd backend
npm install
NODE_ENV=production node server.js

# 2. Test all endpoints
curl http://localhost:3000/health
```

### Step 2: Deploy Database
```bash
# Option A: Railway PostgreSQL
railway add postgresql

# Option B: Supabase (FREE tier)
# Create project at supabase.com
# Get connection string
```

### Step 3: Deploy Backend
```bash
# Railway
railway login
railway init
railway up

# Your backend URL: https://jobika-backend.railway.app
```

### Step 4: Deploy Frontend
```bash
# Update API URL first!
# Then deploy to Vercel
vercel --prod

# Your frontend URL: https://jobika.vercel.app
```

### Step 5: Test in Production
- ✅ Can register/login
- ✅ Can upload resume
- ✅ AI chat works (Gemini)
- ✅ Job search works
- ✅ Application tracking works
- ✅ Resume tailoring works

---

## 📊 POST-DEPLOYMENT

### Monitor
```bash
# Run SRE agent
python3 backend/scripts/async_sre_agent.py 300

# Check health
curl https://your-backend.railway.app/health
```

### Scale
- **Free tier:** 100 users, 1000 req/day
- **Paid tier ($10/mo):** Unlimited

---

## 🔮 FUTURE PHASES (After Production)

### Phase 2: Advanced Features (2-4 weeks)
- [ ] Chrome extension
- [ ] Company insights
- [ ] Email alerts
- [ ] Better job scraping

### Phase 3: Framework Migration (1-2 months)
- [ ] Backend: Express → FastAPI (optional)
- [ ] Frontend: Vanilla JS → Next.js (optional)  
- [ ] Database: Expand schema

### Phase 4: Mobile Apps (3-4 months)
- [ ] React Native iOS
- [ ] React Native Android

---

## 💰 COST ESTIMATE

**Month 1 (FREE):**
- Backend: Railway FREE tier
- Frontend: Vercel FREE tier
- Database: Supabase FREE tier
- AI: Gemini FREE tier (60 req/min)
- **Total: $0/month**

**After Growth (Paid):**
- Backend: $10/month (Railway)
- Database: $25/month (Supabase Pro)
- AI: $50/month (Gemini usage)
- Frontend: Vercel stays free
- **Total: ~$85/month**

---

## 🎯 SUCCESS CRITERIA

**Week 1:**
- [ ] App is live and accessible
- [ ] AI features working
- [ ] Users can register
- [ ] Zero downtime

**Month 1:**
- [ ] 100+ registered users
- [ ] 1000+ job applications submitted
- [ ] <500ms response time
- [ ] 99% uptime

---

## 🆘 TROUBLESHOOTING

**Database connection fails:**
```bash
# Check DATABASE_URL format
postgresql://user:password@host:5432/database?sslmode=require
```

**AI not working:**
```bash
# Verify Gemini API key
curl -H "Authorization: Bearer $GEMINI_API_KEY" \
  https://generativelanguage.googleapis.com/v1beta/models
```

**CORS errors:**
```bash
# Add to .env
ALLOWED_ORIGINS=https://jobika.vercel.app,https://www.jobika.com
```

---

## 📞 SUPPORT

- **Issues:** Check `diagnostics.sh`
- **Logs:** Check Railway/Vercel dashboards  
- **SRE Agent:** Auto-fixes 60% of issues

---

**Next Step:** Deploy to Railway + Vercel TODAY! 🚀
