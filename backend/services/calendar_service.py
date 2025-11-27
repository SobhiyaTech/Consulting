from googleapiclient.discovery import build
from services.auth_service import auth_service
from schemas import EventCreateRequest, EventUpdateRequest, TimeSlot
from datetime import datetime, timedelta
import pytz

class CalendarService:
    def get_service(self):
        creds = auth_service.get_credentials()
        if not creds:
            raise Exception("No valid credentials found. Please authenticate first.")
        return build('calendar', 'v3', credentials=creds)

    def get_free_busy(self, time_min: datetime, time_max: datetime, timezone: str, email: str = 'primary'):
        service = self.get_service()
        body = {
            "timeMin": time_min.isoformat(),
            "timeMax": time_max.isoformat(),
            "timeZone": timezone,
            "items": [{"id": email}]
        }
        events_result = service.freebusy().query(body=body).execute()
        calendars = events_result.get('calendars', {})
        busy_slots = calendars.get(email, {}).get('busy', [])
        
        # Convert busy slots to TimeSlot objects
        busy_times = [
            TimeSlot(
                start=datetime.fromisoformat(slot['start'].replace('Z', '+00:00')),
                end=datetime.fromisoformat(slot['end'].replace('Z', '+00:00'))
            ) for slot in busy_slots
        ]
        
        # Calculate available slots (simple logic: 1-hour slots between 9 AM and 5 PM)
        # Note: This is a simplified availability logic. Real-world logic might be more complex.
        available_slots = self.calculate_available_slots(time_min, time_max, busy_times, timezone)
        
        return busy_times, available_slots

    def calculate_available_slots(self, start_range: datetime, end_range: datetime, busy_slots: list[TimeSlot], timezone: str):
        available = []
        tz = pytz.timezone(timezone)
        
        # Normalize start/end to the requested timezone
        current = start_range.astimezone(tz)
        end_limit = end_range.astimezone(tz)

        # Work hours: 9 AM to 5 PM
        work_start_hour = 9
        work_end_hour = 17
        slot_duration = timedelta(minutes=60)

        while current + slot_duration <= end_limit:
            # Check if current slot is within work hours
            if work_start_hour <= current.hour < work_end_hour:
                slot_end = current + slot_duration
                
                # Check for overlap with busy slots
                is_busy = False
                for busy in busy_slots:
                    # Convert busy slot to same timezone for comparison
                    b_start = busy.start.astimezone(tz)
                    b_end = busy.end.astimezone(tz)
                    
                    if not (slot_end <= b_start or current >= b_end):
                        is_busy = True
                        break
                
                if not is_busy:
                    available.append(TimeSlot(start=current, end=slot_end))
            
            current += slot_duration
            
        return available

    def create_event(self, event_data: EventCreateRequest):
        service = self.get_service()
        event = {
            'summary': event_data.summary,
            'description': event_data.description,
            'start': {
                'dateTime': event_data.start_time.isoformat(),
                'timeZone': event_data.timezone,
            },
            'end': {
                'dateTime': event_data.end_time.isoformat(),
                'timeZone': event_data.timezone,
            },
            'attendees': [
                {'email': event_data.attendee_email},
            ],
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event

    def update_event(self, event_data: EventUpdateRequest):
        service = self.get_service()
        event = service.events().get(calendarId='primary', eventId=event_data.event_id).execute()

        if event_data.summary:
            event['summary'] = event_data.summary
        if event_data.description:
            event['description'] = event_data.description
        if event_data.start_time:
            event['start']['dateTime'] = event_data.start_time.isoformat()
        if event_data.end_time:
            event['end']['dateTime'] = event_data.end_time.isoformat()
        
        updated_event = service.events().patch(calendarId='primary', eventId=event_data.event_id, body=event).execute()
        return updated_event

    def delete_event(self, event_id: str):
        service = self.get_service()
        service.events().delete(calendarId='primary', eventId=event_id).execute()

    def list_events(self, max_results=10, time_min=None):
        service = self.get_service()
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        if time_min:
            now = time_min.isoformat()
            
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=max_results, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

calendar_service = CalendarService()
