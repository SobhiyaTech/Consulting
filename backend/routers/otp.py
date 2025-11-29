from fastapi import APIRouter
from schemas import OTPRequest, OTPVerifyRequest
from services.otp_service import send_otp, verify_otp

router = APIRouter(prefix="/otp", tags=["OTP"])

@router.post("/send-otp")
def send_otp_route(data: OTPRequest):
    otp = send_otp(data.phone)
    return {"success": True, "otp": otp}

@router.post("/verify-otp")
def verify_otp_route(data: OTPVerifyRequest):
    valid = verify_otp(data.phone, data.otp)
    return {"success": valid}
