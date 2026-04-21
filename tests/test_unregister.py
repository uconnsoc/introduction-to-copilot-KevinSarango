"""Tests for the DELETE /activities/{activity_name}/unregister endpoint."""
import pytest


def test_unregister_successful(client, sample_data):
    """Test successful unregister from an activity."""
    activity = sample_data["activities"]["with_participants"]
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]
    assert email in data["message"]


def test_unregister_removes_participant_from_activity(client, sample_data):
    """Test that unregister removes participant from the participants list."""
    activity = sample_data["activities"]["with_participants"]
    email = "michael@mergington.edu"  # Already in Chess Club
    
    # Verify participant is in activity initially
    get_response = client.get("/activities")
    assert email in get_response.json()[activity]["participants"]
    
    # Unregister
    unregister_response = client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    assert unregister_response.status_code == 200
    
    # Verify participant is no longer in activity
    get_response = client.get("/activities")
    assert email not in get_response.json()[activity]["participants"]


def test_unregister_not_signed_up_fails(client, sample_data):
    """Test that unregistering non-enrolled student returns 400."""
    activity = sample_data["activities"]["empty"]  # Basketball Team has no participants
    email = sample_data["emails"]["student1"]
    
    response = client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()


def test_unregister_nonexistent_activity_fails(client, sample_data):
    """Test that unregister for non-existent activity returns 404."""
    activity = "Non Existent Activity"
    email = sample_data["emails"]["student1"]
    
    response = client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_multiple_participants(client, sample_data):
    """Test that unregistering doesn't affect other participants."""
    activity = sample_data["activities"]["with_participants"]
    email_to_remove = "michael@mergington.edu"
    email_to_keep = "daniel@mergington.edu"
    
    # Verify both are in activity
    get_response = client.get("/activities")
    participants = get_response.json()[activity]["participants"]
    assert email_to_remove in participants
    assert email_to_keep in participants
    
    # Unregister one student
    response = client.delete(
        f"/activities/{activity}/unregister?email={email_to_remove}"
    )
    assert response.status_code == 200
    
    # Verify only the correct student was removed
    get_response = client.get("/activities")
    participants = get_response.json()[activity]["participants"]
    assert email_to_remove not in participants
    assert email_to_keep in participants


def test_unregister_returns_success_message(client, sample_data):
    """Test that unregister returns appropriate message."""
    activity = sample_data["activities"]["with_participants"]
    email = "michael@mergington.edu"
    
    response = client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert email in data["message"]
    assert activity in data["message"]
