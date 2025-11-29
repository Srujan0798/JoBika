# 🚂 Railway Deployment - Complete Guide

## ✅ **Option 1: Install Railway CLI (Recommended)**

### Method A: Using Homebrew (Easiest for Mac)
```bash
brew install railway
```

### Method B: Direct Download
```bash
# Download and install manually:
curl -fsSL https://railway.app/install.sh | sh

# If that fails, download from:
# https://github.com/railwayapp/cli/releases
```

### Method C: Using NPM
```bash
npm install -g @railway/cli
```

---

## ✅ **Option 2: Deploy via Railway Dashboard (No CLI needed)**

If CLI installation fails, use the web dashboard:

### Step 1: Go to Railway Dashboard
1. Open: https://railway.app
2. Click "Login" → Login with GitHub
3. Click "New Project"

### Step 2: Deploy from GitHub
1. Click "Deploy from GitHub repo"
2. Select repository: `Srujan0798/JoBika_Pyt`
3. Click "Deploy Now"

### Step 3: Configure Service
1. Click on the deployed service
2. Go to "Settings" tab
3. **Root Directory:** Set to `backend`
4. **Start Command:** `node server.js`

### Step 4: Add Environment Variables
Click "Variables" tab, then add these one by one:

```
DATABASE_TYPE=postgres
DATABASE_URL=postgresql://postgres.eabkwiklxjbqbfxcdlkk:23110081aiiTgn@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
GEMINI_API_KEY=AIzaSyCfUUpFaa5GQ3F45znzykDS-eZNOimfhdg
JWT_SECRET=jobika-production-secret-key-2024
NODE_ENV=production
DATABASE_SSL=true
ALLOWED_ORIGINS=https://jobika.vercel.app
```

### Step 5: Get Your URL
1. Go to "Settings" tab
2. Scroll to "Domains"
3. Click "Generate Domain"
4. **Copy the URL** (e.g., `jobika-backend-production.up.railway.app`)

### Step 6: Verify Deployment
```bash
# Test your backend (replace with YOUR URL):
curl https://YOUR-RAILWAY-URL.up.railway.app/health
```

Should return:
```json
{"status":"ok","database":"connected"}
```

---

## 🎯 **RECOMMENDED: Use Option 2 (Dashboard)**

**Why?**
- ✅ No CLI installation needed
- ✅ Visual interface
- ✅ Easier to manage
- ✅ Same result

**Steps:**
1. Go to https://railway.app
2. Login with GitHub
3. New Project → Deploy from GitHub
4. Select `JoBika_Pyt` repo
5. Set root directory to `backend`
6. Add environment variables
7. Generate domain
8. Copy URL

**That's it!** 🚀

---

## 📊 **After Deployment**

### Check Logs
1. Railway Dashboard → Your Project
2. Click "Deployments" tab
3. View build and runtime logs

### Monitor Status
- Dashboard shows: ✅ Active or ❌ Failed
- Check "Metrics" tab for CPU/Memory usage

### Update Code
```bash
# Just push to GitHub:
git push origin master

# Railway auto-redeploys!
```

---

## 🆘 **Troubleshooting**

### Build Fails
**Check:**
1. Root directory is set to `backend`
2. All environment variables are set
3. `package.json` exists in backend/

**Fix:**
- Settings → Root Directory → `backend`
- Redeploy

### Database Connection Fails
**Check:**
1. DATABASE_URL is correct (port 6543)
2. Supabase project is active
3. DATABASE_SSL=true is set

**Fix:**
- Variables → Update DATABASE_URL
- Redeploy

### App Crashes
**Check logs:**
1. Deployments → View Logs
2. Look for error messages

**Common fixes:**
- Missing environment variable
- Wrong start command
- Port binding issue

---

## 💡 **Pro Tips**

### Custom Domain (Later)
1. Settings → Domains
2. Add custom domain
3. Update DNS records

### Auto-Deploy from GitHub
- Already enabled by default!
- Every `git push` triggers deployment

### Environment Variables
- Can update anytime in Variables tab
- Changes trigger automatic redeploy

---

**Ready to deploy?**

**👉 Go to: https://railway.app and follow Option 2 steps!**

**Or install CLI with: `brew install railway`**
