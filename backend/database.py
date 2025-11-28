import os
import sqlite3
import traceback
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """Get database connection (SQLite or PostgreSQL)"""
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url and database_url.startswith('postgres'):
        # Use PostgreSQL (Supabase/Render)
        try:
            conn = psycopg2.connect(database_url, sslmode='require', cursor_factory=RealDictCursor)
            return conn, 'postgres'
        except Exception as e:
            print(f"❌ Postgres Connection Error: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            raise e
    
    # Use SQLite (Local)
    # print("⚠️ Using SQLite (DATABASE_URL not set or not postgres)")
    conn = sqlite3.connect('jobika.db')
    conn.row_factory = sqlite3.Row
    return conn, 'sqlite'

def get_db():
    """Helper to get just the connection object"""
    conn, _ = get_db_connection()
    return conn

def get_placeholder(db_type):
    """Get SQL placeholder based on DB type"""
    return '%s' if db_type == 'postgres' else '?'

def init_db():
    """Initialize database with all tables (SQLite & PostgreSQL compatible)"""
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    
    # Define ID type based on DB
    id_type = "SERIAL PRIMARY KEY" if db_type == 'postgres' else "INTEGER PRIMARY KEY AUTOINCREMENT"
    text_type = "TEXT"
    bool_type = "BOOLEAN"
    timestamp_default = "DEFAULT CURRENT_TIMESTAMP"
    
    print(f"🔧 Initializing database ({db_type})...")

    # 1. Users table
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS users (
        id {id_type},
        email {text_type} UNIQUE NOT NULL,
        password_hash {text_type} NOT NULL,
        full_name {text_type},
        phone {text_type},
        two_factor_secret {text_type},
        is_two_factor_enabled {bool_type} DEFAULT 0,
        oauth_provider {text_type},
        oauth_id {text_type},
        created_at TIMESTAMP {timestamp_default}
    )''')
    
    # 2. Resumes table
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS resumes (
        id {id_type},
        user_id INTEGER NOT NULL,
        filename {text_type},
        original_text {text_type},
        enhanced_text {text_type},
        skills {text_type},
        experience_years INTEGER,
        created_at TIMESTAMP {timestamp_default},
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # 3. Jobs table
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS jobs (
        id {id_type},
        title {text_type} NOT NULL,
        company {text_type} NOT NULL,
        location {text_type},
        salary {text_type},
        description {text_type},
        required_skills {text_type},
        posted_date {text_type},
        source {text_type},
        created_at TIMESTAMP {timestamp_default}
    )''')
    
    # 4. Applications table
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS applications (
        id {id_type},
        user_id INTEGER NOT NULL,
        job_id INTEGER NOT NULL,
        resume_id INTEGER,
        status {text_type} DEFAULT 'applied',
        match_score INTEGER,
        applied_date {text_type},
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (job_id) REFERENCES jobs(id),
        FOREIGN KEY (resume_id) REFERENCES resumes(id)
    )''')
    
    # 5. Notifications table
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS notifications (
        id {id_type},
        user_id INTEGER NOT NULL,
        title {text_type} NOT NULL,
        message {text_type} NOT NULL,
        type {text_type} DEFAULT 'info',
        is_read {bool_type} DEFAULT 0,
        created_at TIMESTAMP {timestamp_default},
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    # 6. Saved Jobs table
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS saved_jobs (
        id {id_type},
        user_id INTEGER NOT NULL,
        job_id INTEGER NOT NULL,
        created_at TIMESTAMP {timestamp_default},
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (job_id) REFERENCES jobs(id),
        UNIQUE(user_id, job_id)
    )''')

    # 7. Cover Letters table
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS cover_letters (
        id {id_type},
        user_id INTEGER NOT NULL,
        job_id INTEGER NOT NULL,
        content {text_type},
        style {text_type},
        created_at TIMESTAMP {timestamp_default},
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (job_id) REFERENCES jobs(id)
    )''')

    # 8. Job Alerts table
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS job_alerts (
        id {id_type},
        user_id INTEGER NOT NULL,
        keywords {text_type},
        location {text_type},
        frequency {text_type} DEFAULT 'daily',
        is_active {bool_type} DEFAULT 1,
        last_sent_at TIMESTAMP,
        created_at TIMESTAMP {timestamp_default},
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    # 9. Skill Gaps table
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS skill_gaps (
        id {id_type},
        user_id INTEGER NOT NULL,
        job_id INTEGER NOT NULL,
        matching_skills {text_type},
        missing_skills {text_type},
        match_score INTEGER,
        recommendations {text_type},
        created_at TIMESTAMP {timestamp_default},
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (job_id) REFERENCES jobs(id)
    )''')

    # 10. Resume Versions table (for comparison)
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS resume_versions (
        id {id_type},
        user_id INTEGER NOT NULL,
        version_name {text_type},
        content {text_type},
        skills {text_type},
        match_score INTEGER,
        job_id INTEGER,
        created_at TIMESTAMP {timestamp_default},
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized with ALL tables (Auth, Jobs, AI Features)")
