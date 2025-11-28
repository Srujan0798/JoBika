# 🔌 Connect Supabase to Vercel (For Persistent Data)

Currently, your Vercel app uses **SQLite**, which resets every time you deploy.
To save user data permanently, you need to connect **Supabase**.

## 1. Get Connection String from Supabase
1. Go to your [Supabase Dashboard](https://supabase.com/dashboard).
2. Select your project (`JoBika`).
3. Go to **Settings** (Cog icon) > **Database**.
4. Under **Connection String**, select **URI**.
5. **IMPORTANT:** Copy the "Session Mode" string (port 5432) or "Transaction Mode" (port 6543) if you enabled pooling.
   - Format: `postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`
6. Replace `[PASSWORD]` with your actual database password.

## 2. Add to Vercel
1. Go to your [Vercel Dashboard](https://vercel.com/dashboard).
2. Select your project (`jobika-pyt`).
3. Go to **Settings** > **Environment Variables**.
4. Add a new variable:
   - **Key**: `DATABASE_URL`
   - **Value**: (Paste your Supabase connection string)
5. Click **Save**.

## 3. Redeploy
1. Go to **Deployments**.
2. Click the three dots (`...`) on the latest deployment.
3. Select **Redeploy**.

## ✅ Verification
Once redeployed, your app will automatically detect `DATABASE_URL` and switch from SQLite to PostgreSQL.
- User accounts will be saved.
- Resumes will be saved.
- Jobs will be saved.

If the connection fails (e.g., wrong password), the app will **automatically fallback to SQLite** so it never crashes! 🛡️
