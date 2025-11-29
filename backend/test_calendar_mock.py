import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/calendar"

def test_create_event():
    print("\nTesting Create Event...")
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    payload = {
        "summary": "Test Meeting",
        "description": "Discussing project",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "timezone": "UTC",
        "attendee_email": "test@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/create", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get("event_id")

def test_list_events():
    print("\nTesting List Events...")
    response = requests.post(f"{BASE_URL}/list", json={"max_results": 5})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_free_busy():
    print("\nTesting Free/Busy...")
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(days=1)
    
    payload = {
        "time_min": start_time.isoformat(),
        "time_max": end_time.isoformat(),
        "timezone": "UTC",
        "email": "test@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/freebusy", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    try:
        event_id = test_create_event()
        test_list_events()
        test_free_busy()
        print("\nTests Completed Successfully!")
    except Exception as e:
        print(f"\nTests Failed: {e}")
