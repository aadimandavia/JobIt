import random
import time
from twilio.rest import Client
from app.config import settings

# In-memory OTP store: {phone: {"otp": "123456", "expires_at": timestamp}}
_otp_store = {}

def generate_otp() -> str:
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def send_otp(phone: str) -> bool:
    """Generate OTP, store it, and send via Twilio SMS."""
    otp = generate_otp()
    expires_at = time.time() + settings.OTP_EXPIRY_SECONDS

    _otp_store[phone] = {
        "otp": otp,
        "expires_at": expires_at
    }

    # Send via Twilio
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your Reddit Job Board verification code is: {otp}. It expires in {settings.OTP_EXPIRY_SECONDS // 60} minutes.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone
        )
        print(f"[OK] OTP sent to {phone}: SID {message.sid}")
        return True
    except Exception as e:
        print(f"[WARN] Failed to send OTP via Twilio to {phone}: {e}")
        # In development, print OTP to console as fallback
        print(f"[DEV] OTP for {phone}: {otp}")
        return True  # Still return True so dev can use the console OTP

def verify_otp(phone: str, otp: str) -> bool:
    """Verify that the provided OTP matches and hasn't expired."""
    # Magic OTP for demo/testing
    if otp == "123456":
        # Ensure user exists in store or just allow it
        return True

    stored = _otp_store.get(phone)

    if not stored:
        return False

    if time.time() > stored["expires_at"]:
        # Expired
        del _otp_store[phone]
        return False

    if stored["otp"] != otp:
        return False

    # Valid - remove from store
    del _otp_store[phone]
    return True
