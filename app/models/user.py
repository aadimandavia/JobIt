from app.database import get_db
from datetime import datetime

def create_users_table():
    """Create users table if it doesn't exist."""
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email TEXT UNIQUE,
                phone TEXT UNIQUE,
                password_hash TEXT,
                name TEXT DEFAULT '',
                provider TEXT DEFAULT 'manual',
                provider_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Migration: Add columns if they don't exist
        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS email TEXT UNIQUE;")
        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash TEXT;")
        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS provider TEXT DEFAULT 'manual';")
        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS provider_id TEXT;")
        cur.execute("ALTER TABLE users ALTER COLUMN phone DROP NOT NULL;") 
        conn.commit()
        print("[OK] Users table ready")
    except Exception as e:
        print(f"[ERROR] Error creating users table: {e}")
    finally:
        cur.close()
        conn.close()

def find_or_create_user(phone: str, name: str = ""):
    """Find existing user or create new one. Returns user dict."""
    conn = get_db()
    cur = conn.cursor()
    try:
        # Try to find existing user
        cur.execute("SELECT id, phone, name, created_at, last_login FROM users WHERE phone = %s", (phone,))
        row = cur.fetchone()

        if row:
            # Update last login
            cur.execute("UPDATE users SET last_login = %s WHERE phone = %s", (datetime.utcnow(), phone))
            conn.commit()
            return {
                "id": row[0],
                "phone": row[1],
                "name": row[2],
                "created_at": row[3],
                "last_login": row[4]
            }
        else:
            # Create new user
            cur.execute("""
                INSERT INTO users (phone, name, created_at, last_login)
                VALUES (%s, %s, %s, %s)
                RETURNING id, phone, name, created_at, last_login;
            """, (phone, name, datetime.utcnow(), datetime.utcnow()))
            row = cur.fetchone()
            conn.commit()
            print(f"[OK] New user created: {phone}")
            return {
                "id": row[0],
                "phone": row[1],
                "name": row[2],
                "created_at": row[3],
                "last_login": row[4]
            }
    except Exception as e:
        print(f"[ERROR] Error in find_or_create_user: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def get_user_by_phone(phone: str):
    """Lookup user by phone number."""
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, phone, name, created_at, last_login FROM users WHERE phone = %s", (phone,))
        row = cur.fetchone()
        if row:
            return {
                "id": row[0],
                "phone": row[1],
                "name": row[2],
                "created_at": row[3],
                "last_login": row[4]
            }
        return None
    finally:
        cur.close()
        conn.close()

def update_user_name(phone: str, name: str):
    """Update user's display name."""
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET name = %s WHERE phone = %s", (name, phone))
        conn.commit()
        return True
    except Exception as e:
        print(f"[ERROR] Error updating user name: {e}")
        return False
    finally:
        cur.close()
        conn.close()
def get_user_by_email(email: str):
    """Lookup user by email."""
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, email, phone, name, provider, created_at, last_login FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
        if row:
            return {
                "id": row[0],
                "email": row[1],
                "phone": row[2],
                "name": row[3],
                "provider": row[4],
                "created_at": row[5],
                "last_login": row[6]
            }
        return None
    finally:
        cur.close()
        conn.close()

def create_manual_user(email: str, password_hash: str, name: str = ""):
    """Create a new manual user account."""
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO users (email, password_hash, name, provider)
            VALUES (%s, %s, %s, 'manual')
            RETURNING id, email, name, created_at;
        """, (email, password_hash, name))
        row = cur.fetchone()
        conn.commit()
        return {
            "id": row[0],
            "email": row[1],
            "name": row[2],
            "created_at": row[3]
        }
    except Exception as e:
        print(f"[ERROR] create_manual_user failed: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def find_or_create_oauth_user(provider: str, provider_id: str, email: str, name: str):
    """Find or create an OAuth user."""
    conn = get_db()
    cur = conn.cursor()
    try:
        # Try to find by provider_id
        cur.execute("SELECT id, email, name FROM users WHERE provider = %s AND provider_id = %s", (provider, provider_id))
        row = cur.fetchone()
        
        if row:
            # Update last login
            cur.execute("UPDATE users SET last_login = %s WHERE id = %s", (datetime.utcnow(), row[0]))
            conn.commit()
            return {"id": row[0], "email": row[1], "name": row[2]}
        
        # If not found by provider_id, try by email
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        email_row = cur.fetchone()
        
        if email_row:
            # Link existing user to this provider
            cur.execute("UPDATE users SET provider = %s, provider_id = %s, last_login = %s WHERE id = %s", 
                       (provider, provider_id, datetime.utcnow(), email_row[0]))
            conn.commit()
            return {"id": email_row[0], "email": email, "name": name}
            
        # Create new user
        cur.execute("""
            INSERT INTO users (email, name, provider, provider_id, last_login)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (email, name, provider, provider_id, datetime.utcnow()))
        user_id = cur.fetchone()[0]
        conn.commit()
        return {"id": user_id, "email": email, "name": name}
    except Exception as e:
        print(f"[ERROR] find_or_create_oauth_user failed: {e}")
        return None
    finally:
        cur.close()
        conn.close()
