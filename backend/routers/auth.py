from fastapi import APIRouter, Request, HTTPException
from services.auth_service import auth_service
from fastapi.responses import RedirectResponse, HTMLResponse

router = APIRouter(prefix="/oauth", tags=["Auth"])

@router.get("/login")
def login():
    """Redirects user to Google OAuth2 login page."""
    auth_url = auth_service.get_authorization_url()
    return RedirectResponse(auth_url)

@router.get("/callback")
def callback(request: Request):
    """Handles the callback from Google OAuth2."""
    error = request.query_params.get("error")
    if error:
        raise HTTPException(status_code=400, detail=f"OAuth Error: {error}")

    code = request.query_params.get("code")
    if not code:
        print(f"Callback params: {request.query_params}")
        return HTMLResponse(content=f"""
        <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 50px;">
                <h2 style="color: red;">Login Failed</h2>
                <p>No authorization code was received from Google.</p>
                <p>This happens if you visit this page directly or if you denied access.</p>
                <a href="/oauth/login" style="background-color: #4285F4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Try Again</a>
            </body>
        </html>
        """, status_code=400)
    
    try:
        creds = auth_service.fetch_token(code)
        return HTMLResponse(content="""
        <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 50px;">
                <h2 style="color: green;">Authentication Successful!</h2>
                <p>You can now close this window and use the chatbot.</p>
                <p><a href="/docs">View API Documentation</a></p>
            </body>
        </html>
        """)
    except Exception as e:
        return HTMLResponse(content=f"""
        <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 50px;">
                <h2 style="color: red;">Authentication Error</h2>
                <p>Error: {str(e)}</p>
                <a href="/oauth/login" style="background-color: #4285F4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Try Again</a>
            </body>
        </html>
        """, status_code=500)
