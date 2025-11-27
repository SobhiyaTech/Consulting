from fastapi import APIRouter, HTTPException
from services.otp_service import otp_service
from services.email_service import email_service
from schemas import OTPRequest, OTPVerifyRequest, OTPResponse, EmailRequest, EmailResponse

router = APIRouter(tags=["Notifications"])

@router.post("/send-otp", response_model=OTPResponse)
def send_otp(request: OTPRequest):
    result = otp_service.send_otp(request.phone_number)
    return result

@router.post("/verify-otp", response_model=OTPResponse)
def verify_otp(request: OTPVerifyRequest):
    success, message = otp_service.verify_otp(request.phone_number, request.otp)
    return {"status": "success" if success else "error", "message": message}

@router.post("/send-email", response_model=EmailResponse)
def send_email(request: EmailRequest):
    result = email_service.send_email(request.to_email, request.subject, request.body)
    return result
