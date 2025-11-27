# Consulting Services Chatbot Backend

This is a FastAPI backend for a Zoho SalesIQ Chatbot, featuring Google Calendar integration, OTP verification, and Email notifications.

## Features

- **Google Calendar Integration**:
  - OAuth2 Authorization Code Flow
  - Check Free/Busy slots
  - Create, Update, Delete, List events
- **OTP Verification**:
  - Mock implementation (prints to console)
  - Twilio integration (optional)
- **Email Notifications**:
  - Mock implementation (prints to console)
  - SendGrid integration (optional)

## Setup

1.  **Clone the repository**
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment**:
    - Copy `.env.example` to `.env`
    - Fill in your Google OAuth credentials (Client ID, Secret, Redirect URI)
    - (Optional) Fill in Twilio/SendGrid credentials
4.  **Run the Server**:
    ```bash
    uvicorn main:app --reload
    ```

## Google OAuth Setup

1.  Go to [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a project and enable **Google Calendar API**.
3.  Configure OAuth Consent Screen.
4.  Create OAuth 2.0 Credentials (Web Application).
5.  Add `http://localhost:8000/oauth/callback` to Authorized Redirect URIs.
6.  Download credentials or copy Client ID/Secret to `.env`.

## API Documentation

Once running, visit `http://localhost:8000/docs` for the interactive Swagger UI.

## Deployment

This project is ready for deployment on platforms like Render, Railway, or PythonAnywhere.
- **Render/Railway**: Connect your repo, set the build command to `pip install -r requirements.txt` and start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`. Add environment variables in the dashboard.
- **PythonAnywhere**: Upload files, set up a virtualenv, install requirements, and configure the WSGI file to point to `main:app`.

## Zobot Integration

Use the `invokeurl` task in Deluge to call these endpoints.
Example:
```deluge
response = invokeurl
[
    url: "https://your-app-url.com/calendar/freebusy"
    type: POST
    parameters: "{\"time_min\": \"...\", \"time_max\": \"...\"}"
];
```
