import json
import os
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from config import settings

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']

class AuthService:
    def __init__(self):
        self.creds = None
        self.token_file = settings.TOKEN_STORAGE_FILE
        self.client_config = {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
            }
        }

    def get_authorization_url(self):
        """Generates the Google OAuth2 authorization URL."""
        flow = Flow.from_client_config(
            self.client_config,
            scopes=SCOPES,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        auth_url, _ = flow.authorization_url(access_type='offline', include_granted_scopes='true')
        return auth_url

    def fetch_token(self, code: str):
        """Exchanges the authorization code for tokens."""
        flow = Flow.from_client_config(
            self.client_config,
            scopes=SCOPES,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        flow.fetch_token(code=code)
        self.creds = flow.credentials
        self.save_credentials(self.creds)
        return self.creds

    def save_credentials(self, creds):
        """Saves credentials to a file."""
        data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
        with open(self.token_file, 'w') as f:
            json.dump(data, f)

    def load_credentials(self):
        """Loads credentials from file and refreshes if necessary."""
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as f:
                data = json.load(f)
                self.creds = Credentials.from_authorized_user_info(data, SCOPES)
        
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
            self.save_credentials(self.creds)
            
        return self.creds

    def get_credentials(self):
        """Returns valid credentials, loading/refreshing if needed."""
        if not self.creds or not self.creds.valid:
            self.load_credentials()
        return self.creds

auth_service = AuthService()
