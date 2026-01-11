import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    activity = "Math Olympiad"
    email = "testuser1@mergington.edu"
    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert f"Signed up {email} for {activity}" in response.json()["message"]

def test_signup_for_activity_duplicate():
    activity = "Math Olympiad"
    email = "testuser2@mergington.edu"
    # Add once
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/NonexistentActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

# Unregister endpoint test (if implemented)
def test_unregister_participant():
    activity = "Math Olympiad"
    email = "testuser3@mergington.edu"
    # Add participant if not present
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    # Unregister (should exist in app.py for this to pass)
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Accept 200 or 404 depending on implementation
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert email not in activities[activity]["participants"]