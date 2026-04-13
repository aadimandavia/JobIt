from fastapi import APIRouter, Response, Depends
from app.config import settings
from app.schemas.user_schema import SendOTPRequest, VerifyOTPRequest, UserResponse, UpdateNameRequest, RegisterRequest, LoginRequest
from app.utils.otp_handler import send_otp, verify_otp
from app.utils.jwt_handler import create_access_token, get_current_user
from app.models.user import find_or_create_user, update_user_name, create_manual_user, get_user_by_email, find_or_create_oauth_user
from app.utils.password_handler import hash_password, verify_password
from app.utils.oauth_handler import GoogleOAuthHandler
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/send-otp")
def send_otp_endpoint(request: SendOTPRequest):
    """Send OTP to the provided phone number."""
    phone = request.phone.strip()

    if not phone or len(phone) < 10:
        return {"success": False, "message": "Invalid phone number"}

    success = send_otp(phone)

    if success:
        return {"success": True, "message": "OTP sent successfully"}
    else:
        return {"success": False, "message": "Failed to send OTP. Please try again."}

@router.post("/verify-otp")
def verify_otp_endpoint(request: VerifyOTPRequest, response: Response):
    """Verify OTP and issue JWT token as cookie."""
    phone = request.phone.strip()
    otp = request.otp.strip()

    if not verify_otp(phone, otp):
        return {"success": False, "message": "Invalid or expired OTP"}

    # Create or find user
    user = find_or_create_user(phone)
    if not user:
        return {"success": False, "message": "Failed to create user account"}

    # Issue JWT
    token = create_access_token({"phone": user["phone"], "user_id": user["id"]})

    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=86400,  # 24 hours
        samesite="none",
        secure=True,
        path="/"
    )

    return {
        "success": True,
        "message": "Logged in successfully",
        "user": {
            "id": user["id"],
            "phone": user.get("phone"),
            "email": user.get("email"),
            "name": user["name"]
        }
    }

@router.post("/register")
def register_endpoint(request: RegisterRequest, response: Response):
    """Register a new user manually."""
    # Check if user already exists
    if get_user_by_email(request.email):
        return {"success": False, "message": "Email already registered"}
    
    # Hash password
    hashed = hash_password(request.password)
    
    # Create user
    user = create_manual_user(request.email, hashed, request.name)
    if not user:
        return {"success": False, "message": "Failed to create user"}
    
    # Issue JWT
    token = create_access_token({"email": user["email"], "user_id": user["id"]})
    
    # Set Cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=86400,
        samesite="none",
        secure=True,
        path="/"
    )
    
    return {
        "success": True,
        "message": "Account created successfully",
        "user": user
    }

@router.post("/login")
def login_endpoint(request: LoginRequest, response: Response):
    """Log in manually with email and password."""
    user = get_user_by_email(request.email)
    
    if not user:
        return {"success": False, "message": "Invalid email or password"}
    
    # Check if this is actually a manual user (and has a password hash)
    if not user.get("password_hash"):
        return {"success": False, "message": "Please use Google to log in for this account"}
    
    # Verify password
    if not verify_password(request.password, user["password_hash"]):
        return {"success": False, "message": "Invalid email or password"}
    
    # Issue JWT
    token = create_access_token({"email": user["email"], "user_id": user["id"]})
    
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=86400,
        samesite="none",
        secure=True,
        path="/"
    )
    
    return {
        "success": True,
        "message": "Logged in successfully",
        "user": {"id": user["id"], "email": user["email"], "name": user["name"]}
    }

@router.get("/google/login")
def google_login():
    """Redirect to Google for authentication."""
    url = GoogleOAuthHandler.get_login_url()
    return RedirectResponse(url=url)

@router.get("/google/callback")
def google_callback(code: str):
    """Handle Google OAuth callback."""
    # 1. Get tokens
    token_data = GoogleOAuthHandler.get_token(code)
    if not token_data:
        return RedirectResponse(url="/login?error=google_failed")
    
    # 2. Get user info
    user_info = GoogleOAuthHandler.get_user_info(token_data["access_token"])
    if not user_info:
        return RedirectResponse(url="/login?error=google_userinfo_failed")
    
    # 3. Find or create user
    email = user_info.get("email")
    name = user_info.get("name", "")
    provider_id = user_info.get("sub")
    
    user = find_or_create_oauth_user("google", provider_id, email, name)
    
    # 4. Issue JWT
    token = create_access_token({"email": user["email"], "user_id": user["id"]})
    
    # 5. Redirect to dashboard (frontend) and set cookie
    response = RedirectResponse(url=f"{settings.FRONTEND_URL}/dashboard")
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=86400,
        samesite="none",
        secure=True,
        path="/"
    )
    
    return response

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """Get current logged-in user info."""
    from app.models.user import get_user_by_phone, get_user_by_email
    
    email = current_user.get("email")
    phone = current_user.get("phone")
    
    user = None
    if email:
        user = get_user_by_email(email)
    elif phone:
        user = get_user_by_phone(phone)
        
    if not user:
        return {"success": False, "message": "User not found"}
    
    return {
        "success": True,
        "user": user
    }

@router.post("/update-name")
def update_name_endpoint(request: UpdateNameRequest, current_user: dict = Depends(get_current_user)):
    """Update the current user's display name."""
    success = update_user_name(current_user["phone"], request.name)
    if success:
        return {"success": True, "message": "Name updated"}
    return {"success": False, "message": "Failed to update name"}

@router.post("/logout")
def logout(response: Response):
    """Clear the JWT cookie."""
    response.delete_cookie("access_token", path="/")
    return {"success": True, "message": "Logged out successfully"}
