from config import settings
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

class EmailService:
    def send_email(self, to_email: str, subject: str, body: str):
        # Mock sending
        print(f"Mock Email to {to_email}: Subject: {subject}, Body: {body}")
        
        # Real SendGrid sending (if configured)
        if settings.SENDGRID_API_KEY and settings.FROM_EMAIL:
            try:
                sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
                from_email = Email(settings.FROM_EMAIL)
                to_email_obj = To(to_email)
                content = Content("text/plain", body)
                mail = Mail(from_email, to_email_obj, subject, content)
                response = sg.client.mail.send.post(request_body=mail.get())
                return {"status": "success", "message": "Email sent via SendGrid", "code": response.status_code}
            except Exception as e:
                print(f"SendGrid Error: {e}")
                return {"status": "error", "message": str(e)}

        return {"status": "success", "message": "Email logged (check console for mock)"}

email_service = EmailService()
