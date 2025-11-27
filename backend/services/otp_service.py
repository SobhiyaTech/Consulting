import random
import string
from datetime import datetime, timedelta
from typing import Dict
from config import settings

# In-memory storage for OTPs (for demonstration purposes)
# In production, use Redis or a database
otp_storage: Dict[str, Dict] = {}

class OTPService:
    def generate_otp(self, length=6):
        return ''.join(random.choices(string.digits, k=length))

    def send_otp(self, phone_number: str):
        otp = self.generate_otp()
        expiry = datetime.now() + timedelta(minutes=5)
        otp_storage[phone_number] = {"otp": otp, "expiry": expiry}
        
        # Mock sending
        print(f"Mock OTP for {phone_number}: {otp}")
        
        # Real Twilio sending (if configured)
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN and settings.TWILIO_PHONE_NUMBER:
            try:
                from twilio.rest import Client
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f"Your verification code is {otp}",
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=phone_number
                )
                return {"status": "success", "message": "OTP sent via Twilio", "sid": message.sid}
            except Exception as e:
                print(f"Twilio Error: {e}")
                return {"status": "error", "message": str(e)}

        return {"status": "success", "message": "OTP generated (check console for mock)"}

    def verify_otp(self, phone_number: str, otp: str):
        record = otp_storage.get(phone_number)
        if not record:
            return False, "OTP not found or expired"
        
        if datetime.now() > record["expiry"]:
            del otp_storage[phone_number]
            return False, "OTP expired"
        
        if record["otp"] == otp:
            del otp_storage[phone_number]
            return True, "OTP verified successfully"
        
        return False, "Invalid OTP"

otp_service = OTPService()
