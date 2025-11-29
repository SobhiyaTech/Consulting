import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    TOKEN_STORAGE_FILE: str = "token.json"

    # Twilio (Optional)
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None

    # SendGrid (Optional)
    SENDGRID_API_KEY: Optional[str] = None
    FROM_EMAIL: Optional[str] = None

    # App
    APP_ENV: str = "development"
    USE_MOCK_CALENDAR: bool = False

    # Gemini API
    GEMINI_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
