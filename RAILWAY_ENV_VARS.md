# 🚨 RAILWAY ENVIRONMENT VARIABLES - REQUIRED!

## ❌ Current Issue:
```
502 Bad Gateway - Application failed to respond
```

**Cause:** Missing environment variables in Railway Dashboard.

---

## ✅ **SOLUTION: Add These Environment Variables**

Go to **Railway Dashboard** → Your Backend Service → **Variables** tab

### **Add ALL of these:**

```bash
# Database (Supabase)
DATABASE_TYPE=postgres
DATABASE_URL=postgresql://postgres.eabkwiklxjbqbfxcdlkk:23110081aiiTgn@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
DATABASE_SSL=require
SUPABASE_URL=https://eabkwiklxjbqbfxcdlkk.supabase.co

# Gemini AI
GEMINI_API_KEY=AIzaSyCfUUpFaa5GQ3F45znzykDS-eZNOimfhdg

# JWT Secret
JWT_SECRET=jobika-production-secret-key-2024

# Environment
NODE_ENV=production

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://jobika.vercel.app

# Puppeteer (CRITICAL!)
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Vercel
VERCEL_PROJECT_ID=prj_cBYpfrWqhTiJAiI3KlVD6cSINqaG
```

---

## 📝 **Step-by-Step:**

1. **Open Railway Dashboard**
2. **Click on your backend service**
3. **Go to "Variables" tab**
4. **Click "+ New Variable"** for EACH variable above
5. **Copy-paste** the name and value exactly
6. **Click "Add"** after each one
7. **Railway will auto-redeploy** after you add all variables

---

## ⚠️ **IMPORTANT NOTES:**

### **Database URL:**
Use the **Connection Pooling** URL (port 6543), NOT the direct connection (port 5432):
```
postgresql://postgres.eabkwiklxjbqbfxcdlkk:23110081aiiTgn@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

### **Puppeteer Path:**
This is **CRITICAL** - without it, Puppeteer will crash:
```
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
```

---

## ✅ **After Adding All Variables:**

1. Railway will **auto-redeploy** (takes ~2-3 minutes)
2. Test again:
   ```bash
   curl https://jobika-backend-production.up.railway.app/health
   ```
3. Should return:
   ```json
   {"status":"ok","database":"connected"}
   ```

---

## 🎯 **Quick Copy-Paste Format:**

For faster setup, here's the format Railway accepts:

```
DATABASE_TYPE=postgres
DATABASE_URL=postgresql://postgres.eabkwiklxjbqbfxcdlkk:23110081aiiTgn@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
DATABASE_SSL=require
SUPABASE_URL=https://eabkwiklxjbqbfxcdlkk.supabase.co
GEMINI_API_KEY=AIzaSyCfUUpFaa5GQ3F45znzykDS-eZNOimfhdg
JWT_SECRET=jobika-production-secret-key-2024
NODE_ENV=production
ALLOWED_ORIGINS=http://localhost:3000,https://jobika.vercel.app
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
VERCEL_PROJECT_ID=prj_cBYpfrWqhTiJAiI3KlVD6cSINqaG
```

**Add these NOW and your deployment will work!** 🚀
