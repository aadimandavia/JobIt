import os
import requests
from fastapi import HTTPException
from app.config import settings

class GoogleOAuthHandler:
    CLIENT_ID = settings.GOOGLE_CLIENT_ID
    CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
    REDIRECT_URI = settings.GOOGLE_REDIRECT_URI
    
    AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    @classmethod
    def get_login_url(cls):
        params = {
            "client_id": cls.CLIENT_ID,
            "redirect_uri": cls.REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "select_account"
        }
        url = requests.Request("GET", cls.AUTHORIZATION_URL, params=params).prepare().url
        return url

    @classmethod
    def get_token(cls, code):
        data = {
            "client_id": cls.CLIENT_ID,
            "client_secret": cls.CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": cls.REDIRECT_URI,
        }
        response = requests.post(cls.TOKEN_URL, data=data)
        if response.status_code != 200:
            print(f"[ERROR] Google token error: {response.text}")
            return None
        return response.json()

    @classmethod
    def get_user_info(cls, access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(cls.USERINFO_URL, headers=headers)
        if response.status_code != 200:
            print(f"[ERROR] Google userinfo error: {response.text}")
            return None
        return response.json()
