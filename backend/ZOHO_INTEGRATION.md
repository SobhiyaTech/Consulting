# Zoho SalesIQ Integration Guide

Now that your backend is running and authenticated, you can connect it to your Zobot using **Deluge**.

## Base URL
Replace `https://your-backend-url.com` with your actual deployed URL (e.g., on Render/Railway).
If testing locally with ngrok, use your ngrok URL.

## 1. Check Availability (Free/Busy)
Use this code in a Zobot Action to check for available slots.

```deluge
// Input: date (String in YYYY-MM-DD format)
// Output: List of available slots

backend_url = "https://your-backend-url.com";
start_time = date + "T09:00:00";
end_time = date + "T17:00:00";

payload = Map();
payload.put("time_min", start_time);
payload.put("time_max", end_time);
payload.put("timezone", "UTC"); // Change to your timezone if needed

response = invokeurl
[
    url: backend_url + "/calendar/freebusy"
    type: POST
    parameters: payload.toString()
    headers: {"Content-Type": "application/json"}
];

if (response.get("available_slots").size() > 0) {
    // Process available slots
    info response.get("available_slots");
} else {
    info "No slots available.";
}
```

## 2. Book an Appointment
Use this code to create a calendar event.

```deluge
// Input: name, email, date, time
backend_url = "https://your-backend-url.com";

// Format start and end time (assuming 1 hour duration)
start_datetime = date + "T" + time + ":00";
// You might need logic to calculate end_time based on start_time
end_datetime = date + "T" + (time.toLong() + 1) + ":00"; 

payload = Map();
payload.put("summary", "Consultation with " + name);
payload.put("description", "Booked via Zobot");
payload.put("start_time", start_datetime);
payload.put("end_time", end_datetime);
payload.put("attendee_email", email);
payload.put("timezone", "UTC");

response = invokeurl
[
    url: backend_url + "/calendar/create"
    type: POST
    parameters: payload.toString()
    headers: {"Content-Type": "application/json"}
];

if (response.get("status") == "confirmed") {
    info "Booking successful! Link: " + response.get("html_link");
} else {
    info "Booking failed.";
}
```

## 3. Send OTP (Optional)
If you want to verify phone numbers.

```deluge
phone = "+1234567890";
payload = Map();
payload.put("phone_number", phone);

response = invokeurl
[
    url: backend_url + "/send-otp"
    type: POST
    parameters: payload.toString()
    headers: {"Content-Type": "application/json"}
];
```
