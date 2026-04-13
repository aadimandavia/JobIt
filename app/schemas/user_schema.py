from pydantic import BaseModel, EmailStr
from typing import Optional

class SendOTPRequest(BaseModel):
    phone: str

class VerifyOTPRequest(BaseModel):
    phone: str
    otp: str

class UserResponse(BaseModel):
    id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = ""
    provider: Optional[str] = "manual"

class UpdateNameRequest(BaseModel):
    name: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = ""

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
