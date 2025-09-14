# database/db_utils.py

import sqlite3
import hashlib
import os
from typing import Dict, Any

# Database path (relative to project root)
DB_PATH = os.path.join(os.path.dirname(__file__), "alumni.db")

def init_db():
    """
    Initialize the SQLite database and create the alumni table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            skills TEXT,           -- JSON array as string: ["Python", "SQL"]
            experience TEXT,       -- JSON object as string: [{"job_title": "...", ...}]
            projects TEXT,         -- JSON object as string
            education TEXT,        -- JSON object as string
            courses TEXT,          -- JSON array as string
            social_media TEXT,     -- JSON object as string: {"linkedin": "...", ...}
            resume_hash TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized at: {DB_PATH}")

def save_alumni(profile: Dict[str, Any], name: str = "Unknown"):
    """
    Save a parsed alumni profile into the database.
    Avoids duplicates using resume_hash.
    """
    init_db()  # Ensure DB exists
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Generate hash from key fields to detect duplicates
    resume_content = f"{profile.get('email', '')}{profile.get('phone', '')}{str(profile.get('skills', []))}"
    resume_hash = hashlib.sha256(resume_content.encode()).hexdigest()

    try:
        cursor.execute('''
            INSERT OR IGNORE INTO alumni 
            (name, email, phone, skills, experience, projects, education, courses, social_media, resume_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name,
            profile.get('email', ''),
            profile.get('phone', ''),
            str(profile.get('skills', [])),           # Convert list → string
            str(profile.get('experience', [])),       # Convert list of dicts → string
            str(profile.get('projects', [])),         # Same
            str(profile.get('education', [])),        # Same
            str(profile.get('courses', [])),          # Same
            str(profile.get('social_media', {})),     # Convert dict → string
            resume_hash
        ))
        
        if cursor.rowcount == 0:
            print(f"⚠️ Duplicate resume detected (hash: {resume_hash}) — skipped.")
        else:
            print(f"✅ Saved alumni: {profile.get('email', 'N/A')} (ID: {cursor.lastrowid})")
        
        conn.commit()
        
    except sqlite3.IntegrityError as e:
        print(f"❌ Integrity error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error saving profile: {e}")
    finally:
        conn.close()

def get_all_alumni():
    """
    Fetch all alumni records (for dashboard).
    Returns list of dicts with converted JSON strings back to Python objects.
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM alumni ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for row in rows:
        record = dict(row)
        # Convert stored strings back to Python objects
        for key in ['skills', 'experience', 'projects', 'education', 'courses', 'social_media']:
            try:
                import json
                if record[key]:
                    record[key] = json.loads(record[key])
                else:
                    record[key] = [] if key in ['skills', 'experience', 'projects', 'education', 'courses'] else {}
            except:
                record[key] = [] if key in ['skills', 'experience', 'projects', 'education', 'courses'] else {}
        result.append(record)
    
    return result

def get_alumni_by_email(email: str):
    """
    Find a single alumni record by email.
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM alumni WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    record = dict(row)
    for key in ['skills', 'experience', 'projects', 'education', 'courses', 'social_media']:
        try:
            import json
            if record[key]:
                record[key] = json.loads(record[key])
            else:
                record[key] = [] if key in ['skills', 'experience', 'projects', 'education', 'courses'] else {}
        except:
            record[key] = [] if key in ['skills', 'experience', 'projects', 'education', 'courses'] else {}
    return record