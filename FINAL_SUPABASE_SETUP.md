# 🚀 Final Step: Connect Render to Supabase (PostgreSQL)

Follow these exact steps to switch from SQLite to your production Supabase database.

## Step 1: Get Your Connection String
1. Log in to your **Supabase Dashboard**.
2. Click on your project **JoBika_Pyt**.
3. **IMPORTANT**: If the project says "Paused", click **"Restore Project"** and wait for it to turn green (Active).
4. Go to **Project Settings** (gear icon) -> **Database** -> **Connection string**.
5. Click **URI** and copy the string. It looks like this:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.eabkwiklxjbqbfxcdlkk.supabase.co:5432/postgres
   ```
   *(Replace `[YOUR-PASSWORD]` with `23110081aiiTgn` if that is your DB password)*

## Step 2: Update Render Configuration
1. Go to your **Render Dashboard** -> **JoBika_Pyt**.
2. Click **Environment** (left menu).
3. Click **"Add Environment Variable"**.
4. Enter:
   - **Key**: `DATABASE_URL`
   - **Value**: *(Paste the connection string from Step 1)*
5. Click **"Save Changes"**.

## Step 3: Redeploy
1. Click **Manual Deploy** (top right).
2. Select **"Clear build cache & deploy"**.

## That's it! 🎉
- Render will restart.
- The app will detect `DATABASE_URL` and automatically connect to Supabase.
- It will create all necessary tables (Users, Jobs, Resumes, etc.) automatically on the first run.
- Your app is now fully production-ready with a persistent PostgreSQL database!
