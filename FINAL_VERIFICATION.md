# JoBika - Final Production Verification Checklist

## ✅ CRITICAL CHECKS BEFORE DEPLOYMENT

### 1. Indian Market Localization (Current Implementation)

**✅ Already Implemented:**
- Salary in INR (LPA format)
- CTC-aware AI (Orion understands Indian context)
- Notice period handling
- Indian job sources (Naukri, LinkedIn India references)
- Experience terms (fresher=0-1 years)

**⚠️ To Verify:**
```bash
# Check Orion AI context
grep -r "CTC\|notice period\|LPA" backend/services/OrionCoachService.js

# Verify Indian English
grep -r "Indian" backend/services/
```

**Action Items:**
- [ ] Test: Ask Orion "What's a good CTC for 3 years experience?"
- [ ] Test: Resume includes notice period field
- [ ] Verify: Salary displays as "₹10-15 LPA"

---

### 2. Database Schema (Simple → Production)

**Current Schema (SQLite):**
```sql
users, applications, jobs, resumes, chat_history
```

**Missing for Production:**
```sql
-- Add these tables:
user_education
user_experience  
user_skills
companies
saved_jobs
job_alerts
application_events
```

**Migration Script:**
```bash
# Create: backend/database/postgres_schema.sql
# Run: node backend/database/migrate.js
```

**Action Items:**
- [ ] Create full PostgreSQL schema
- [ ] Test migration script
- [ ] Backup current SQLite data

---

### 3. API Endpoints Verification

**✅ Implemented:**
```
POST /api/auth/register
POST /api/auth/login
GET  /api/jobs
POST /api/resume/tailor
POST /api/chat
GET  /api/applications
GET  /health
```

**⚠️ Missing (Add if needed):**
```javascript
// backend/server.js - Add these:

// Saved jobs
app.post('/api/saved-jobs', authMiddleware, async (req, res) => {
  const { jobId } = req.body;
  await db.saveJob(req.user.id, jobId);
  res.json({ success: true });
});

app.get('/api/saved-jobs', authMiddleware, async (req, res) => {
  const saved = await db.getSavedJobs(req.user.id);
  res.json(saved);
});

// Job alerts
app.post('/api/alerts', authMiddleware, validate(alertSchema), async (req, res) => {
  const alert = await db.createAlert(req.user.id, req.validated);
  res.json(alert);
});

// Dashboard stats
app.get('/api/users/dashboard-stats', authMiddleware, async (req, res) => {
  const stats = await db.getDashboardStats(req.user.id);
  res.json(stats);
});
```

**Action Items:**
- [ ] Add missing endpoints (10 min each)
- [ ] Test all endpoints with Postman
- [ ] Add to API documentation

---

### 4. Environment Variables Check

**Required for Production:**
```bash
# .env - VERIFY THESE EXIST:
GEMINI_API_KEY=xxx                    # ✅ EXISTS
DATABASE_TYPE=postgres                # ⚠️  SET FOR PRODUCTION
DATABASE_URL=postgresql://...         # ⚠️  ADD FOR PRODUCTION
JWT_SECRET=xxx                        # ✅ EXISTS
NODE_ENV=production                   # ⚠️  SET FOR DEPLOYMENT
ALLOWED_ORIGINS=https://jobika.com    # ⚠️  ADD YOUR DOMAIN

# OPTIONAL (for future):
RAZORPAY_KEY_ID=xxx                   # Payment (Phase 2)
SMTP_HOST=smtp.gmail.com              # Email alerts (Phase 2)
WHATSAPP_API_KEY=xxx                  # WhatsApp alerts (Phase 3)
```

**Action Items:**
- [x] Verify Gemini API key works
- [ ] Generate strong JWT secret
- [ ] Get PostgreSQL connection string
- [ ] Configure CORS origins

---

### 5. Pricing Implementation (Basic)

**Current:** FREE tier only

**Add Simple Tier Logic:**
```javascript
// backend/middleware/subscription.js
function checkSubscriptionTier(req, res, next) {
  const userTier = req.user.subscriptionTier || 'free';
  
  const limits = {
    free: { dailyApplications: 5, aiChats: 5 },
    pro: { dailyApplications: 50, aiChats: -1 },
    premium: { dailyApplications: -1, aiChats: -1, agentEnabled: true }
  };
  
  req.userLimits = limits[userTier];
  next();
}

// Usage:
app.post('/api/apply', authMiddleware, checkSubscriptionTier, (req, res) => {
  if (req.user.todayApplications >= req.userLimits.dailyApplications) {
    return res.status(402).json({ 
      error: 'Daily limit reached. Upgrade to Pro!' 
    });
  }
  // ... apply logic
});
```

**Action Items:**
- [ ] Add subscription_tier to users table
- [ ] Implement rate limiting per tier
- [ ] Add "Upgrade" prompts in UI

---

### 6. Job Scraping (Simplified for MVP)

**Current:** Manual job data

**Simple Scraper (Start Small):**
```javascript
// backend/services/SimpleJobScraper.js
const puppeteer = require('puppeteer');

class SimpleJobScraper {
  async scrapeNaukri(keyword = 'software engineer', location = 'bangalore') {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    const url = `https://www.naukri.com/${keyword}-jobs-in-${location}`;
    await page.goto(url);
    
    const jobs = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('.jobTuple')).map(el => ({
        title: el.querySelector('.title')?.innerText,
        company: el.querySelector('.companyInfo')?.innerText,
        experience: el.querySelector('.expwdth')?.innerText,
        salary: el.querySelector('.salary')?.innerText,
        location: el.querySelector('.locWdth')?.innerText
      }));
    });
    
    await browser.close();
    return jobs;
  }
}

// Run daily via cron
// 0 9 * * * node backend/scripts/daily_scrape.js
```

**Action Items:**
- [ ] Test scraper locally
- [ ] Add to cron job (later)
- [ ] For MVP: Use sample job data

---

### 7. Frontend Indian Localization

**Add to UI:**
```javascript
// app/assets/js/formatter.js
function formatSalary(min, max) {
  return `₹${min/100000}-${max/100000} LPA`;
}

function formatExperience(months) {
  const years = Math.floor(months / 12);
  if (years === 0) return 'Fresher';
  return `${years} ${years === 1 ? 'year' : 'years'}`;
}

function formatNoticePeriod(days) {
  if (days === 0) return 'Immediate joiner';
  return `${days} days`;
}
```

**Action Items:**
- [ ] Replace "$" with "₹" everywhere
- [ ] Use "LPA" instead of "per year"
- [ ] Add notice period to profile

---

### 8. Testing Before Launch

**Manual Tests (15 min checklist):**
```bash
# 1. Auth Flow
- [ ] Register new user
- [ ] Login
- [ ] Logout
- [ ] Forgot password (if implemented)

# 2. Resume
- [ ] Upload PDF resume
- [ ] Parse shows correct data
- [ ] Tailor for a job
- [ ] Download tailored version

# 3. AI Chat
- [ ] Ask: "What's a good CTC for 5 years experience?"
- [ ] Ask: "Review my resume"
- [ ] Ask: "Prepare for TCS interview"

# 4. Jobs
- [ ] Search for jobs
- [ ] Filter by location
- [ ] View job details
- [ ] Save a job
- [ ] Apply to job

# 5. Applications
- [ ] View application tracker
- [ ] Update status
- [ ] Add notes

# 6. Performance
- [ ] Page load < 2s
- [ ] API response < 500ms
- [ ] No console errors
```

**Action Items:**
- [ ] Run all manual tests
- [ ] Fix any bugs found
- [ ] Test on mobile browser

---

### 9. Deployment Readiness

**Pre-Flight Checklist:**
```bash
# Code Quality
[ ] No console.log in production code
[ ] No hardcoded API keys
[ ] All .env variables documented
[ ] Git repo clean (no sensitive files)

# Security
[ ] HTTPS enabled
[ ] CORS configured
[ ] Rate limiting active
[ ] Input validation on all endpoints
[ ] SQL injection prevention verified

# Monitoring
[ ] Health check endpoint works
[ ] SRE agent configured
[ ] Error logging setup
[ ] Performance monitoring ready

# Documentation
[ ] README.md complete
[ ] API documentation exists
[ ] Deployment guide written
[ ] Production checklist done
```

---

### 10. Launch Day Operations

**Deployment Steps:**
```bash
# 1. Deploy database
railway add postgresql
# Save connection string

# 2. Deploy backend
git push railway master
# Verify: curl https://api.jobika.com/health

# 3. Deploy frontend
vercel --prod
# Verify: Open https://jobika.com

# 4. Start monitoring
python3 backend/scripts/async_sre_agent.py &

# 5. Monitor logs
railway logs --tail
vercel logs

# 6. Test critical paths
- Registration
- AI chat
- Resume upload
```

**Rollback Plan:**
```bash
# If anything breaks:
railway rollback
vercel rollback

# Revert database:
pg_restore backup.dump
```

---

## 📊 FINAL STATUS

### ✅ Production Ready:
- Core authentication
- AI features (Gemini)
- Resume tailoring
- Application tracking
- Basic job search
- Security middleware

### ⚠️ Needs Minor Updates:
- Add saved jobs endpoint
- Add dashboard stats endpoint
- Format currency as INR/LPA
- Simple subscription tiers

### ❌ Future Features (Post-MVP):
- Job scraping automation
- Chrome extension
- Company insights
- Mock interviews
- Payment integration
- Mobile apps

---

## 🎯 DEPLOY PRIORITY

**Week 1 (NOW):**
1. Verify current features work
2. Add missing simple endpoints
3. Deploy to Railway + Vercel
4. Test in production

**Week 2-4:**
5. Add job scraping
6. Implement tier limits
7. Add saved jobs
8. Email notifications

**Month 2-3:**
9. Payment integration
10. Chrome extension
11. Advanced features

---

**BOTTOM LINE:** Your app is 90% ready. Just needs:
1. PostgreSQL setup (1 hour)
2. Add 3-4 missing endpoints (2 hours)
3. Indian formatting (1 hour)
4. Deploy! (2 hours)

**Total time to production: 1 day** 🚀
