from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# --- OTP Schemas ---
class OTPRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number in E.164 format (e.g., +1234567890)")

class OTPVerifyRequest(BaseModel):
    phone_number: str
    otp: str

class OTPResponse(BaseModel):
    status: str
    message: str

# --- Email Schemas ---
class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    body: str

class EmailResponse(BaseModel):
    status: str
    message: str

# --- Calendar Schemas ---
class FreeBusyRequest(BaseModel):
    time_min: datetime
    time_max: datetime
    timezone: str = "UTC"
    email: Optional[EmailStr] = None # Optional specific calendar ID, defaults to primary

class TimeSlot(BaseModel):
    start: datetime
    end: datetime

class FreeBusyResponse(BaseModel):
    busy_slots: List[TimeSlot]
    available_slots: List[TimeSlot] # Calculated available slots

class EventCreateRequest(BaseModel):
    summary: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    attendee_email: EmailStr
    timezone: str = "UTC"

class EventUpdateRequest(BaseModel):
    event_id: str
    summary: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    timezone: str = "UTC"

class EventResponse(BaseModel):
    event_id: str
    html_link: str
    status: str
    summary: str
    start: datetime
    end: datetime

class EventListRequest(BaseModel):
    email: Optional[EmailStr] = None
    max_results: int = 10
    time_min: Optional[datetime] = None

class DeleteEventRequest(BaseModel):
    event_id: str
