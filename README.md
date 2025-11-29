# JoBika - AI-Powered Job Application Platform

> **Production-ready job search platform with AI resume tailoring and auto-apply capabilities**

## 🎯 Overview

JoBika is an enterprise-grade job application platform that uses AI to:
- **Tailor resumes** automatically for each job posting
- **Auto-apply** to matching positions
- **AI career coaching** (Orion) for interview prep and career guidance
- **ATS score checking** to optimize resume success rates
- **Application tracking** with transparency and analytics

Built for the Indian job market with understanding of CTC, notice periods, and local hiring practices.

---

## 📁 Project Structure

```
JoBika_Pyt/
├── app/                          # Frontend (Vanilla JS)
│   ├── assets/
│   │   ├── css/
│   │   │   ├── index.css         # Design system & variables
│   │   │   └── ux-states.css     # Loading, error, empty states
│   │   └── js/
│   │       ├── api.js            # Backend API client
│   │       ├── errorHandling.js  # Error boundaries & recovery
│   │       └── performance.js    # Web Vitals monitoring
│   ├── index.html                # Landing page (public)
│   ├── dashboard.html            # Main dashboard
│   ├── jobs.html                 # Job search & browse
│   ├── chat.html                 # AI career coach (Orion)
│   ├── tracker.html              # Application tracking
│   ├── login.html                # Authentication
│   └── signup.html
│
├── backend/                      # Node.js + Express
│   ├── config/
│   │   ├── agent_config.toml     # SRE agent configuration
│   │   └── common_failures.json  # 350+ error patterns
│   ├── database/
│   │   ├── db.js                 # Universal DB manager (SQLite/Postgres)
│   │   ├── schema.sql            # Database schema
│   │   └── jobika.db             # SQLite database (dev)
│   ├── middleware/
│   │   ├── security.js           # XSS, CSRF, rate limiting
│   │   └── validation.js         # Zod input validation
│   ├── services/
│   │   ├── GeminiService.js      # Google Gemini AI integration
│   │   ├── ResumeTailoringService.js
│   │   ├── OrionCoachService.js  # AI career coach
│   │   ├── ATSService.js         # ATS score checker
│   │   ├── JobScraper.js         # Job aggregation
│   │   ├── ApplicationFormFiller.js  # Auto-apply automation
│   │   └── AuthService.js        # JWT authentication
│   ├── utils/
│   │   ├── errorHandler.js       # Global error handling
│   │   ├── resiliencePatterns.js # Circuit breaker, retry, etc.
│   │   └── fixTemplates.js       # Production patterns
│   ├── scripts/
│   │   ├── async_sre_agent.py    # Autonomous SRE agent
│   │   └── diagnostics.sh        # System health check
│   └── server.js                 # Main server file
│
├── .env                          # Environment variables
├── package.json                  # Node.js dependencies
├── docker-compose.yml            # Docker setup
└── README.md                     # This file
```

---

## 🚀 Quick Start

### **Prerequisites**
- Node.js 18+ 
- Python 3.8+ (for SRE agent)
- Google Gemini API key (free at https://aistudio.google.com/app/apikey)

### **1. Install Dependencies**
```bash
# Backend
cd backend
npm install

# Python dependencies (for SRE agent - optional)
pip3 install requests
```

### **2. Configure Environment**
```bash
# Copy and edit .env file
cp .env.example .env

# Required: Add your Gemini API key
GEMINI_API_KEY=your_key_here

# Optional: Database (defaults to SQLite)
DATABASE_TYPE=sqlite  # or postgres for production
```

### **3. Initialize Database**
```bash
cd backend
node -e "const db = require('./database/db'); new db();"
```

### **4. Start Development Server**
```bash
cd backend
node server.js
```

Server runs at `http://localhost:3000`

### **5. (Optional) Start SRE Agent**
```bash
# Run autonomous monitoring & auto-fix
python3 backend/scripts/async_sre_agent.py 300  # 5 hours
```

---

## 🔧 Configuration

### **Environment Variables**

```bash
# === AI Configuration ===
GEMINI_API_KEY=your_gemini_key  # Required for AI features

# === Database ===
DATABASE_TYPE=sqlite                    # sqlite | postgres
DATABASE_PATH=./backend/database/jobika.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:pass@host:5432/dbname
# DATABASE_SSL=true

# === Server ===
PORT=3000
NODE_ENV=development  # development | production

# === Security ===
JWT_SECRET=your_secret_key
JWT_EXPIRES_IN=7d
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# === SRE Agent (Optional) ===
SRE_LLM_PROVIDER=gemini  # gemini | openai | claude
SRE_SAFETY_MODE=true
SRE_MAX_FIXES_PER_HOUR=10
```

---

## 💻 Development

### **Run Tests**
```bash
cd backend
npm test
```

### **Check System Health**
```bash
./backend/scripts/diagnostics.sh
```

### **Monitor Performance**
- Web Vitals tracked automatically in browser console
- Backend metrics at `/health` endpoint

### **Debugging**
```bash
# Enable debug logging
NODE_ENV=development node server.js

# Check database
sqlite3 backend/database/jobika.db "SELECT * FROM users LIMIT 5;"

# Monitor logs
tail -f server.log
```

---

## 🚢 Production Deployment

### **1. Build for Production**
```bash
NODE_ENV=production npm start
```

### **2. Database Migration (PostgreSQL)**
```bash
# Set DATABASE_TYPE=postgres in .env
# Run migrations
node backend/database/migrate.js
```

### **3. Deploy Options**

#### **Vercel (Frontend + Serverless)**
```bash
vercel deploy
```

#### **Railway/Render (Full Stack)**
- Connect GitHub repository
- Set environment variables in dashboard
- Auto-deploys on push

#### **Docker**
```bash
docker-compose up -d
```

---

## 🔒 Security Features

- ✅ **Input Validation** - Zod schemas on all endpoints
- ✅ **SQL Injection Prevention** - Parameterized queries only
- ✅ **XSS Protection** - Helmet + sanitization
- ✅ **CSRF Protection** - Token validation
- ✅ **Rate Limiting** - 100 req/min per IP
- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **HTTPS Enforcement** - Production mode
- ✅ **Security Headers** - CSP, HSTS, X-Frame-Options

---

## 🎯 Key Features

### **1. AI Resume Tailoring**
- Customizes resume for each job posting
- Keyword optimization for ATS
- Industry-specific formatting
- Generates PDF automatically

### **2. Auto-Apply System**
- Fills application forms automatically
- Uploads tailored resume
- Handles multi-step forms
- Supervised & autonomous modes

### **3. Orion AI Coach**
- Career guidance for Indian market
- Interview preparation
- Salary negotiation (CTC-aware)
- Resume improvement suggestions

### **4. Application Tracking**
- Real-time status updates
- Response rate analytics
- Company insights
- Follow-up reminders

### **5. Meta-Grade SRE System**
- 350+ error pattern detection
- Autonomous issue resolution
- Circuit breakers & retry logic
- Graceful degradation

---

## 📊 API Documentation

### **Public Endpoints** (No auth required)
```
GET  /api/jobs/public       # Browse jobs
POST /api/chat/demo         # Try AI coach (3 free messages)
GET  /health                # System status
```

### **Authenticated Endpoints**
```
POST /api/auth/register     # Create account
POST /api/auth/login        # Login
GET  /api/applications      # User's applications
POST /api/resume/tailor     # Tailor resume for job
POST /api/auto-apply        # Auto-apply to job
POST /api/chat              # Chat with Orion
POST /api/ats/check         # Check ATS score
```

---

## 🛠️ Tech Stack

**Frontend:**
- Vanilla JavaScript (no frameworks)
- Modern CSS (CSS Variables, Grid, Flexbox)
- Web Vitals monitoring

**Backend:**
- Node.js + Express
- SQLite (dev) / PostgreSQL (prod)
- Google Gemini AI (free tier)
- JWT authentication
- Puppeteer (auto-apply automation)

**DevOps:**
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Vercel/Railway deployment
- Python SRE agent for monitoring

---

## 📈 Performance

- **LCP:** < 2.5s (Largest Contentful Paint)
- **FID:** < 100ms (First Input Delay)
- **CLS:** < 0.1 (Cumulative Layout Shift)
- **Bundle Size:** < 300KB (JavaScript)
- **API Response:** < 500ms (p95)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🆘 Support

**Documentation:**
- [SRE Agent Guide](./SRE_AGENT_README.md)
- [API Documentation](./docs/API.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)

**Issues:**
- GitHub Issues: [Report Bug](https://github.com/yourusername/jobika/issues)

**Contact:**
- Email: support@jobika.com

---

## 🎉 Acknowledgments

Built with insights from production post-mortems:
- Netflix (Circuit Breaker pattern)
- Uber (Exponential Backoff + Jitter)
- Instagram (Graceful Degradation)
- AWS (DNS Failover patterns)
- Slack (Thundering Herd prevention)

---

**Version:** 1.0.0  
**Last Updated:** November 2025  
**Status:** Production Ready ✅
