from app.database import get_db
from datetime import datetime
from app.utils.extractor import extract_stipend

def create_jobs_table():
    """Create jobs table if it doesn't exist."""
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id SERIAL PRIMARY KEY,
                title TEXT,
                subreddit TEXT,
                post_url TEXT UNIQUE,
                created_at TIMESTAMP,
                stipend TEXT,
                description TEXT
            );
        """)
        conn.commit()
        print("[OK] Jobs table ready")
    except Exception as e:
        print(f"[ERROR] Error creating jobs table: {e}")
    finally:
        cur.close()
        conn.close()

def insert_job(job_data: dict):
    conn = get_db()
    cur = conn.cursor()

    stipend = extract_stipend(job_data.get("title", ""))

    try:
        cur.execute("""
            INSERT INTO jobs (title, subreddit, post_url, created_at, stipend, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (post_url) DO NOTHING
            RETURNING id;
        """, (
            job_data["title"],
            job_data["subreddit"],
            job_data["url"],
            datetime.fromtimestamp(job_data["created_at"]),
            stipend,
            job_data.get("description", "")
        ))

        result = cur.fetchone()

        if result:
            # Use safe printing for Windows terminal
            safe_title = job_data['title'].encode('ascii', 'ignore').decode('ascii')
            print(f"[OK] INSERTED: {safe_title}")
            return True
        else:
            safe_title = job_data['title'].encode('ascii', 'ignore').decode('ascii')
            print(f"[SKIP] DUPLICATE: {safe_title}")
            return False

    except Exception as e:
        print(f"[ERROR] Database insertion failed: {e}")
        return False
    finally:
        conn.commit()
        cur.close()
        conn.close()

def get_all_jobs(limit: int = 50, keyword: str = None):
    conn = get_db()
    cur = conn.cursor()

    query = """
        SELECT title, post_url, created_at, stipend, description
        FROM jobs
    """
    params = []

    if keyword:
        query += " WHERE title ILIKE %s "
        params.append(f"%{keyword}%")

    query += " ORDER BY created_at DESC LIMIT %s;"
    params.append(limit)

    cur.execute(query, tuple(params))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "title": r[0],
            "url": r[1],
            "created_at": r[2],
            "stipend": r[3],
            "description": r[4]
        }
        for r in rows
    ]
