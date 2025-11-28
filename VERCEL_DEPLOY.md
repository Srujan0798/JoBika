# 🚀 DEPLOY TO VERCEL

## ✅ Configuration Complete

I've added the necessary files for Vercel deployment:
1. `vercel.json` - Tells Vercel how to run the Flask app
2. `requirements.txt` - Optimized for Vercel (removed Selenium)

## 🔧 Vercel Dashboard Settings

When importing the project in Vercel, use these EXACT settings:

### 1. Project Setup
- **Framework Preset**: `Other` (Do NOT select Flask/Next.js)
- **Root Directory**: `./` (Default)

### 2. Build & Output Settings
- **Build Command**: (Leave Empty)
- **Output Directory**: (Leave Empty)
- **Install Command**: (Leave Empty)

*Vercel automatically detects Python and installs dependencies.*

### 3. Environment Variables (IMPORTANT)
Add these variables in the "Environment Variables" section:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `jobika-production-secret-key-2024` |
| `PYTHON_VERSION` | `3.9` |

### 4. Click "Deploy"

---

## ⚠️ Important Notes for Vercel

1. **Database**: The app will use SQLite by default.
   - **Warning**: SQLite data on Vercel is **read-only** or **ephemeral** (resets on every request/deploy).
   - **Solution**: For persistent data, you MUST connect to Supabase PostgreSQL (see `docs/archive/ENABLE_POOLING_GUIDE.md`).

2. **Job Scraper**:
   - I optimized the scraper to use `requests` instead of `selenium`.
   - It should work fine on Vercel's serverless environment.

3. **Cold Starts**:
   - Vercel functions go to sleep when not used. The first request might take 2-3 seconds to load.

---

## 🎯 Summary

1. Push latest code to GitHub
2. Import in Vercel
3. Set `SECRET_KEY`
4. Deploy!
