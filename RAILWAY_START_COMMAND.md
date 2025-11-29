# 🔧 Railway Settings Configuration

## ⚠️ IMPORTANT: Change Start Command

### Current (WRONG - This is for Python):
```
gunicorn backend.server:app
```

### Change to (CORRECT - For Node.js):
```
node server.js
```

---

## 📋 **Step-by-Step in Railway Dashboard:**

### 1. Go to Settings Tab
- Click on your deployed service
- Click "Settings" in the left sidebar

### 2. Find "Custom Start Command"
- Scroll down to "Deploy" section
- Find "Custom Start Command" field

### 3. Clear Old Command
- **Delete:** `gunicorn backend.server:app`

### 4. Enter New Command
- **Type:** `node server.js`

### 5. Save
- Railway auto-saves
- Will trigger a redeploy

---

## ✅ **Complete Railway Settings Checklist:**

### General Settings:
- [x] **Project Name:** jobika-backend
- [x] **Root Directory:** `backend`

### Deploy Settings:
- [x] **Start Command:** `node server.js` ← **CHANGE THIS**
- [ ] **Build Command:** (leave empty - npm install runs automatically)
- [ ] **Watch Paths:** (leave empty)

### Environment Variables (7 total):
- [x] DATABASE_TYPE=postgres
- [x] DATABASE_URL=postgresql://postgres.eabkwiklxjbqbfxcdlkk:23110081aiiTgn@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
- [x] GEMINI_API_KEY=AIzaSyCfUUpFaa5GQ3F45znzykDS-eZNOimfhdg
- [x] JWT_SECRET=jobika-production-secret-key-2024
- [x] NODE_ENV=production
- [x] DATABASE_SSL=true
- [x] ALLOWED_ORIGINS=https://jobika.vercel.app

---

## 🎯 **Why This Matters:**

**Wrong Command (Python):**
```bash
gunicorn backend.server:app
# ❌ This tries to run Python/Flask
# ❌ Will fail because JoBika is Node.js
```

**Correct Command (Node.js):**
```bash
node server.js
# ✅ Runs Node.js server
# ✅ Works with Express
# ✅ Starts on port from environment
```

---

## 📸 **Visual Guide:**

### Where to Find It:
```
Railway Dashboard
└── Your Project
    └── Service (jobika-backend)
        └── Settings Tab
            └── Deploy Section
                └── Custom Start Command
                    └── [Change here]
```

### What It Should Look Like:
```
┌─────────────────────────────────────┐
│ Custom Start Command                │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ node server.js                  │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Command that will be run to start   │
│ new deployments.                    │
└─────────────────────────────────────┘
```

---

## ⚡ **Quick Fix:**

1. **Delete this:** `gunicorn backend.server:app`
2. **Type this:** `node server.js`
3. **Done!** Railway will redeploy automatically

---

## 🔍 **How to Verify:**

After changing and redeploying:

1. **Check Logs:**
   - Deployments tab → View Logs
   - Should see: `🚀 Server running on port 3000`
   - Should see: `✅ PostgreSQL connected`

2. **Test Health Endpoint:**
   ```bash
   curl https://YOUR-RAILWAY-URL.up.railway.app/health
   ```
   
   Should return:
   ```json
   {"status":"ok","database":"connected"}
   ```

---

## 🆘 **If It Still Fails:**

### Check These:
1. ✅ Root Directory = `backend`
2. ✅ Start Command = `node server.js`
3. ✅ All 7 environment variables set
4. ✅ `package.json` exists in backend/
5. ✅ `server.js` exists in backend/

### View Build Logs:
- Deployments → Click on latest deployment
- Check for errors in build phase
- Check for errors in start phase

---

**Change the command now and Railway will redeploy! 🚀**
