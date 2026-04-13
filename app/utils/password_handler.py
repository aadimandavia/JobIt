import hashlib
import bcrypt

def _get_hashable_password(password: str) -> bytes:
    """Pre-process password to bypass bcrypt's 72-byte limit."""
    # We use SHA-256 then encode to hex and then to bytes for bcrypt
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pw_hash.encode("utf-8")

def hash_password(password: str) -> str:
    """Hash a raw password."""
    # bcrypt expects bytes
    pw_bytes = _get_hashable_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw_bytes, salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed one."""
    try:
        pw_bytes = _get_hashable_password(plain_password)
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(pw_bytes, hashed_bytes)
    except Exception as e:
        print(f"[ERROR] verify_password failed: {e}")
        return False
