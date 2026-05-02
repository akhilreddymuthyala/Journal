from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import psycopg2
import psycopg2.extras

from database import get_connection, init_db

# ── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(title="Journal API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Init DB on startup ───────────────────────────────────────────────────────
@app.on_event("startup")
def startup():
    init_db()

# ── Schemas ──────────────────────────────────────────────────────────────────
class EntryCreate(BaseModel):
    title: str
    content: str
    mood: Optional[str] = None

# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Journal API is running"}

@app.get("/entries")
def get_entries():
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM journal_entries ORDER BY created_at DESC;")
        entries = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(e) for e in entries]
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/entries", status_code=201)
def create_entry(entry: EntryCreate):
    if not entry.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    if not entry.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            """INSERT INTO journal_entries (title, content, mood)
               VALUES (%s, %s, %s) RETURNING *;""",
            (entry.title.strip(), entry.content.strip(), entry.mood)
        )
        new_entry = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return dict(new_entry)
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/entries/{entry_id}")
def delete_entry(entry_id: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM journal_entries WHERE id = %s RETURNING id;",
            (entry_id,)
        )
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if not deleted:
            raise HTTPException(status_code=404, detail="Entry not found")
        return {"deleted": entry_id}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")