#!/bin/bash
# Deploy script for Supabase schema and data seeding

echo "============================================================"
echo "JoBika Production Deployment Script"
echo "============================================================"
echo ""
echo "This script will help you deploy to Supabase + Render"
echo ""

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  DATABASE_URL is not set"
    echo ""
    echo "Please set it first:"
    echo "export DATABASE_URL='your-supabase-connection-string'"
    echo ""
    echo "Get your connection string from:"
    echo "Supabase Dashboard → Project Settings → Database → Connection Pooling"
    echo "Use the 'Transaction' mode connection string (port 6543)"
    echo ""
    exit 1
fi

echo "✅ DATABASE_URL is set"
echo ""

# Step 1: Apply schema
echo "📊 Step 1: Applying database schema..."
echo ""
read -p "Do you want to apply the schema to Supabase? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Applying schema..."
    psql "$DATABASE_URL" < backend/supabase_schema.sql
    if [ $? -eq 0 ]; then
        echo "✅ Schema applied successfully"
    else
        echo "❌ Schema application failed"
        exit 1
    fi
else
    echo "⏭️  Skipping schema application"
fi

echo ""

# Step 2: Seed data
echo "🌱 Step 2: Seeding database..."
echo ""
read -p "Do you want to seed the database with initial data? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Seeding data..."
    python3 backend/seed_data.py
    if [ $? -eq 0 ]; then
        echo "✅ Data seeded successfully"
    else
        echo "❌ Data seeding failed"
        exit 1
    fi
else
    echo "⏭️  Skipping data seeding"
fi

echo ""

# Step 3: Verify
echo "🔍 Step 3: Verifying deployment..."
echo ""
python3 -c "
from backend.database import get_db_connection
conn, db_type = get_db_connection()
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM salary_roles')
count = cursor.fetchone()
print(f'✅ Database connected: {db_type}')
print(f'✅ Salary roles count: {count[0] if count else 0}')
conn.close()
"

echo ""
echo "============================================================"
echo "✅ Deployment Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Commit and push your changes to GitHub"
echo "2. Go to Render dashboard and trigger a manual deploy"
echo "3. Verify the live application"
echo ""
