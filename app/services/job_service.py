from app.database import get_db
from datetime import datetime
from app.utils.extractor import extract_stipend

def insert_job(job):
    conn = get_db()
    cur = conn.cursor()

    stipend = extract_stipend(job["title"])

    try:
        cur.execute("""
            INSERT INTO jobs (title, subreddit, post_url, created_at, stipend, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (post_url) DO NOTHING
            RETURNING id;
        """, (
            job["title"],
            job["subreddit"],
            job["url"],
            datetime.fromtimestamp(job["created_at"]),
            stipend,
            job.get("description", "")
        ))

        result = cur.fetchone()

        if result:
            print("✅ INSERTED:", job["title"])
        else:
            print("⚠️ DUPLICATE:", job["title"])

        conn.commit()

    except Exception as e:
        print("❌ ERROR:", e)

    cur.close()
    conn.close()


def get_all_jobs(limit=50):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT title, post_url, created_at, stipend
        FROM jobs
        ORDER BY created_at DESC
        LIMIT %s;
    """, (limit,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "title": r[0],
            "url": r[1],
            "created_at": r[2],
            "stipend": r[3]
        }
        for r in rows
    ]