"""Tests for the GET /activities endpoint."""
import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that activities dict is returned
    assert isinstance(data, dict)
    assert len(data) > 0
    
    # Check for expected activities
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Soccer Club",
        "Art Club",
        "Drama Club",
        "Debate Club",
        "Science Club"
    ]
    
    for activity in expected_activities:
        assert activity in data


def test_get_activities_has_correct_structure(client):
    """Test that each activity has the correct structure."""
    response = client.get("/activities")
    data = response.json()
    
    # Check the structure of an activity
    activity = data["Chess Club"]
    
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    
    assert isinstance(activity["description"], str)
    assert isinstance(activity["schedule"], str)
    assert isinstance(activity["max_participants"], int)
    assert isinstance(activity["participants"], list)


def test_get_activities_includes_participants(client):
    """Test that activities include enrolled participants."""
    response = client.get("/activities")
    data = response.json()
    
    # Chess Club has initial participants
    chess_club = data["Chess Club"]
    assert len(chess_club["participants"]) > 0
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]
    
    # Basketball Team starts with no participants
    basketball = data["Basketball Team"]
    assert len(basketball["participants"]) == 0
