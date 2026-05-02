import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

# Load .env from the same directory as this file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "127.0.0.1"),
    "port":     os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "journaldb"),
    "user":     os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"[DB ERROR] Could not connect to PostgreSQL: {e}")
        raise

def init_db():
    print(f"[DB] Connecting to {DB_CONFIG['host']}:{DB_CONFIG['port']} / {DB_CONFIG['database']} as {DB_CONFIG['user']}")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id         SERIAL PRIMARY KEY,
            title      VARCHAR(255) NOT NULL,
            content    TEXT NOT NULL,
            mood       VARCHAR(50),
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("[DB] Table ready.")