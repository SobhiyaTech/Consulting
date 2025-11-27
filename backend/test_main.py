from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Consulting Services Chatbot Backend is running"}

def test_send_otp_mock():
    response = client.post("/send-otp", json={"phone_number": "+1234567890"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_verify_otp_fail():
    response = client.post("/verify-otp", json={"phone_number": "+1234567890", "otp": "000000"})
    assert response.status_code == 200
    assert response.json()["status"] == "error"

@patch("services.calendar_service.calendar_service.get_free_busy")
def test_free_busy_mock(mock_get_free_busy):
    mock_get_free_busy.return_value = ([], [])
    response = client.post("/calendar/freebusy", json={
        "time_min": "2023-10-27T09:00:00",
        "time_max": "2023-10-27T17:00:00",
        "timezone": "UTC"
    })
    assert response.status_code == 200
    assert "available_slots" in response.json()
