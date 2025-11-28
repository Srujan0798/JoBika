"""
Database connection module with automatic fallback to SQLite
"""
import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """
    Get database connection.
    Prioritizes PostgreSQL (if DATABASE_URL is set).
    Falls back to SQLite (if connection fails or no URL).
    """
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        try:
            conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
            return conn, 'postgres'
        except Exception as e:
            print(f"⚠️  PostgreSQL connection failed: {e}")
            print("🔄 Falling back to SQLite...")
    
    # SQLite Fallback
    print("📦 Using SQLite database")
    
    # On Vercel (read-only filesystem), use /tmp
    if os.environ.get('VERCEL'):
        db_path = '/tmp/jobika.db'
    else:
        db_path = 'jobika.db'
        
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn, 'sqlite'

def get_placeholder(db_type):
    """Get SQL placeholder for the database type"""
    if db_type == 'postgres':
        return '%s'
    return '?'

def init_db():
    """Initialize database with schema"""
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    
    print(f"🔧 Initializing database ({db_type})...")
    
    # Read schema
    schema_file = os.path.join(os.path.dirname(__file__), 'supabase_schema.sql')
    if not os.path.exists(schema_file):
        print("❌ Schema file not found!")
        return

    with open(schema_file, 'r') as f:
        schema_sql = f.read()

    try:
        if db_type == 'postgres':
            # Execute full schema for Postgres
            cursor.execute(schema_sql)
        else:
            # Convert PostgreSQL schema to SQLite
            # Handle case-insensitive replacements
            schema_sql = schema_sql.replace('SERIAL PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
            schema_sql = schema_sql.replace('serial primary key', 'INTEGER PRIMARY KEY AUTOINCREMENT')
            
            schema_sql = schema_sql.replace('TIMESTAMP DEFAULT CURRENT_TIMESTAMP', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            
            schema_sql = schema_sql.replace('TEXT[]', 'TEXT')
            schema_sql = schema_sql.replace('JSONB', 'TEXT')
            schema_sql = schema_sql.replace('jsonb', 'TEXT')
            
            schema_sql = schema_sql.replace('BOOLEAN', 'INTEGER')
            schema_sql = schema_sql.replace('boolean', 'INTEGER')
            
            schema_sql = schema_sql.replace('TRUE', '1')
            schema_sql = schema_sql.replace('true', '1')
            
            schema_sql = schema_sql.replace('FALSE', '0')
            schema_sql = schema_sql.replace('false', '0')
            
            # Execute each statement
            for statement in schema_sql.split(';'):
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        cursor.execute(statement)
                    except sqlite3.OperationalError as e:
                        if 'already exists' not in str(e):
                            print(f"⚠️  Schema warning: {e}")
                            print(f"Statement: {statement[:50]}...")
        
        conn.commit()
        print(f"✅ Database initialized ({db_type}) with ALL tables")
        
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
    finally:
        conn.close()
