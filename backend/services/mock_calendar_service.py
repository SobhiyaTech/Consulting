from datetime import datetime, timedelta
from schemas import EventCreateRequest, EventUpdateRequest, TimeSlot
import uuid
import random

class MockCalendarService:
    def __init__(self):
        self.events = {}  # In-memory storage for events

    def get_free_busy(self, time_min: datetime, time_max: datetime, timezone: str, email: str = 'primary'):
        # Simulate some busy slots
        busy_times = []
        current = time_min
        while current < time_max:
            if random.choice([True, False]):
                end = current + timedelta(hours=1)
                busy_times.append(TimeSlot(start=current, end=end))
            current += timedelta(hours=2)
        
        # Simulate available slots (inverse of busy, simplified)
        available_slots = []
        current = time_min
        while current < time_max:
            end = current + timedelta(hours=1)
            # Check if this slot overlaps with any busy slot
            is_busy = False
            for busy in busy_times:
                if not (end <= busy.start or current >= busy.end):
                    is_busy = True
                    break
            
            if not is_busy:
                available_slots.append(TimeSlot(start=current, end=end))
            current += timedelta(hours=1)

        return busy_times, available_slots

    def create_event(self, event_data: EventCreateRequest):
        event_id = str(uuid.uuid4())
        event = {
            'id': event_id,
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
            'status': 'confirmed',
            'htmlLink': f'https://calendar.google.com/calendar/event?eid={event_id}'
        }
        self.events[event_id] = event
        print(f"Mock Event Created: {event}")
        return event

    def update_event(self, event_data: EventUpdateRequest):
        if event_data.event_id not in self.events:
            # Create a dummy one if not found for testing flexibility
            self.events[event_data.event_id] = {
                'id': event_data.event_id,
                'status': 'confirmed',
                'htmlLink': f'https://calendar.google.com/calendar/event?eid={event_data.event_id}',
                'start': {}, 'end': {}
            }
        
        event = self.events[event_data.event_id]

        if event_data.summary:
            event['summary'] = event_data.summary
        if event_data.description:
            event['description'] = event_data.description
        if event_data.start_time:
            event['start']['dateTime'] = event_data.start_time.isoformat()
        if event_data.end_time:
            event['end']['dateTime'] = event_data.end_time.isoformat()
        
        print(f"Mock Event Updated: {event}")
        return event

    def delete_event(self, event_id: str):
        if event_id in self.events:
            del self.events[event_id]
        print(f"Mock Event Deleted: {event_id}")

    def list_events(self, max_results=10, time_min=None):
        return list(self.events.values())[:max_results]

mock_calendar_service = MockCalendarService()
