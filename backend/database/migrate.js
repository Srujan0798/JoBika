#!/usr/bin/env node

/**
 * SQLite to PostgreSQL Migration Script
 * Migrates existing JoBika data to production PostgreSQL database
 */

const sqlite3 = require('better-sqlite3');
const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');

// Configuration
const SQLITE_PATH = process.env.SQLITE_PATH || path.join(__dirname, 'jobika.db');
const POSTGRES_URL = process.env.DATABASE_URL || process.env.POSTGRES_URL;

if (!POSTGRES_URL) {
    console.error('❌ DATABASE_URL or POSTGRES_URL environment variable required');
    console.error('Example: export DATABASE_URL="postgresql://user:password@host:5432/database"');
    process.exit(1);
}

const pgPool = new Pool({
    connectionString: POSTGRES_URL,
    ssl: process.env.DATABASE_SSL === 'true' ? { rejectUnauthorized: false } : false
});

async function migrate() {
    console.log('🚀 Starting JoBika SQLite → PostgreSQL Migration\n');

    // Check if SQLite database exists
    if (!fs.existsSync(SQLITE_PATH)) {
        console.error(`❌ SQLite database not found at: ${SQLITE_PATH}`);
        process.exit(1);
    }

    const sqliteDb = sqlite3(SQLITE_PATH);

    try {
        // Test PostgreSQL connection
        console.log('🔌 Testing PostgreSQL connection...');
        await pgPool.query('SELECT NOW()');
        console.log('✅ PostgreSQL connected\n');

        // Run schema creation
        console.log('📋 Creating PostgreSQL schema...');
        const schemaSQL = fs.readFileSync(path.join(__dirname, 'postgres_schema.sql'), 'utf-8');
        await pgPool.query(schemaSQL);
        console.log('✅ Schema created\n');

        // Migrate Users
        console.log('👤 Migrating users...');
        const users = sqliteDb.prepare('SELECT * FROM users').all();
        for (const user of users) {
            await pgPool.query(`
                INSERT INTO users (
                    id, email, password_hash, phone, full_name, 
                    current_city, current_company, current_title,
                    created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                ON CONFLICT (id) DO NOTHING
            `, [
                user.id,
                user.email,
                user.password_hash,
                user.phone,
                user.full_name,
                user.current_city,
                user.current_company,
                user.current_title,
                user.created_at,
                user.updated_at
            ]);
        }
        console.log(`✅ Migrated ${users.length} users\n`);

        // Migrate Jobs
        console.log('💼 Migrating jobs...');
        const jobs = sqliteDb.prepare('SELECT * FROM jobs').all();
        for (const job of jobs) {
            await pgPool.query(`
                INSERT INTO jobs (
                    id, title, company_name, location, job_type, work_mode,
                    description, salary_min, salary_max, posted_date, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ON CONFLICT (id) DO NOTHING
            `, [
                job.id,
                job.title,
                job.company_name,
                job.location,
                job.job_type,
                job.work_mode,
                job.description,
                job.salary_min,
                job.salary_max,
                job.posted_date,
                job.created_at
            ]);
        }
        console.log(`✅ Migrated ${jobs.length} jobs\n`);

        // Migrate Resumes
        console.log('📄 Migrating resumes...');
        const resumes = sqliteDb.prepare('SELECT * FROM resumes').all();
        for (const resume of resumes) {
            await pgPool.query(`
                INSERT INTO resumes (
                    id, user_id, name, is_primary, summary, 
                    ats_score, created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (id) DO NOTHING
            `, [
                resume.id,
                resume.user_id,
                resume.name,
                resume.is_primary,
                resume.summary,
                resume.ats_score,
                resume.created_at,
                resume.updated_at
            ]);
        }
        console.log(`✅ Migrated ${resumes.length} resumes\n`);

        // Migrate Applications
        console.log('📨 Migrating applications...');
        const applications = sqliteDb.prepare('SELECT * FROM applications').all();
        for (const app of applications) {
            await pgPool.query(`
                INSERT INTO applications (
                    id, user_id, job_id, status, applied_via,
                    applied_at, created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (id) DO NOTHING
            `, [
                app.id,
                app.user_id,
                app.job_id,
                app.status,
                app.applied_via,
                app.applied_at,
                app.created_at,
                app.updated_at
            ]);
        }
        console.log(`✅ Migrated ${applications.length} applications\n`);

        // Migrate Chat History
        console.log('💬 Migrating chat messages...');
        const chats = sqliteDb.prepare('SELECT * FROM chat_history').all();
        for (const chat of chats) {
            await pgPool.query(`
                INSERT INTO chat_messages (
                    id, user_id, session_id, role, content, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (id) DO NOTHING
            `, [
                chat.id,
                chat.user_id,
                chat.session_id,
                chat.role,
                chat.content,
                chat.created_at
            ]);
        }
        console.log(`✅ Migrated ${chats.length} chat messages\n`);

        // Verify migration
        console.log('🔍 Verifying migration...');
        const pgUserCount = await pgPool.query('SELECT COUNT(*) FROM users');
        const pgJobCount = await pgPool.query('SELECT COUNT(*) FROM jobs');
        const pgAppCount = await pgPool.query('SELECT COUNT(*) FROM applications');

        console.log(`✅ PostgreSQL has ${pgUserCount.rows[0].count} users`);
        console.log(`✅ PostgreSQL has ${pgJobCount.rows[0].count} jobs`);
        console.log(`✅ PostgreSQL has ${pgAppCount.rows[0].count} applications`);

        console.log('\n✨ Migration completed successfully!');
        console.log('\n📝 Next steps:');
        console.log('1. Update .env: DATABASE_TYPE=postgres');
        console.log('2. Backup SQLite: cp backend/database/jobika.db jobika.db.backup');
        console.log('3. Test app with PostgreSQL');
        console.log('4. Deploy to production\n');

    } catch (error) {
        console.error('\n❌ Migration failed:', error);
        console.error('\nRollback if needed:');
        console.error('DROP DATABASE jobika; CREATE DATABASE jobika;');
        process.exit(1);
    } finally {
        sqliteDb.close();
        await pgPool.end();
    }
}

// Run migration
if (require.main === module) {
    migrate().catch(console.error);
}

module.exports = { migrate };
