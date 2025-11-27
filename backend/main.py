from fastapi import FastAPI
from routers import auth, calendar, notifications
from config import settings

app = FastAPI(
    title="Consulting Services Chatbot Backend",
    description="Backend for Zoho SalesIQ Chatbot with Google Calendar Integration",
    version="1.0.0"
)

# Include Routers
app.include_router(auth.router)
app.include_router(calendar.router)
app.include_router(notifications.router)

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>Consulting Chatbot Backend</title>
        </head>
        <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 50px;">
            <h1>Consulting Services Chatbot Backend</h1>
            <p>Backend is running successfully.</p>
            <a href="/oauth/login" style="background-color: #4285F4; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-size: 18px;">Login with Google</a>
            <br><br>
            <p>After login, you will be redirected back here.</p>
            <p><a href="/docs">View API Documentation</a></p>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
