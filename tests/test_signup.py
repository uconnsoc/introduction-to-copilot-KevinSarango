"""Tests for the POST /activities/{activity_name}/signup endpoint."""
import pytest


def test_signup_successful(client, sample_data):
    """Test successful signup for an activity."""
    activity = sample_data["activities"]["empty"]
    email = sample_data["emails"]["student1"]
    
    response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_signup_adds_participant_to_activity(client, sample_data):
    """Test that signup adds participant to the participants list."""
    activity = sample_data["activities"]["empty"]
    email = sample_data["emails"]["student1"]
    
    # Verify participant not in activity initially
    get_response = client.get("/activities")
    assert email not in get_response.json()[activity]["participants"]
    
    # Sign up
    signup_response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    assert signup_response.status_code == 200
    
    # Verify participant is now in activity
    get_response = client.get("/activities")
    assert email in get_response.json()[activity]["participants"]


def test_signup_duplicate_participant_fails(client, sample_data):
    """Test that duplicate signup is rejected with 400 error."""
    activity = sample_data["activities"]["with_participants"]
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_fails(client, sample_data):
    """Test that signup for non-existent activity returns 404."""
    activity = "Non Existent Activity"
    email = sample_data["emails"]["student1"]
    
    response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_multiple_students_success(client, sample_data):
    """Test that multiple students can sign up for the same activity."""
    activity = sample_data["activities"]["empty"]
    email1 = sample_data["emails"]["student1"]
    email2 = sample_data["emails"]["student2"]
    
    # Sign up first student
    response1 = client.post(f"/activities/{activity}/signup?email={email1}")
    assert response1.status_code == 200
    
    # Sign up second student
    response2 = client.post(f"/activities/{activity}/signup?email={email2}")
    assert response2.status_code == 200
    
    # Verify both are in activity
    get_response = client.get("/activities")
    participants = get_response.json()[activity]["participants"]
    assert email1 in participants
    assert email2 in participants
    assert len(participants) == 2


def test_signup_returns_success_message(client, sample_data):
    """Test that signup returns appropriate message."""
    activity = sample_data["activities"]["empty"]
    email = sample_data["emails"]["student1"]
    
    response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert email in data["message"]
    assert activity in data["message"]
