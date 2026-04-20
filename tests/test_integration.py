"""Integration tests for the activity registration system."""
import pytest


def test_signup_then_get_activities_workflow(client, sample_data):
    """Test signup followed by getting activities shows new participant."""
    activity = sample_data["activities"]["empty"]
    email = sample_data["emails"]["student1"]
    
    # Initial state - student not in activity
    get_response = client.get("/activities")
    assert email not in get_response.json()[activity]["participants"]
    
    # Sign up
    signup_response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    assert signup_response.status_code == 200
    
    # Verify in activities list
    get_response = client.get("/activities")
    assert email in get_response.json()[activity]["participants"]


def test_signup_unregister_workflow(client, sample_data):
    """Test complete workflow: signup -> unregister."""
    activity = sample_data["activities"]["empty"]
    email = sample_data["emails"]["student1"]
    
    # Sign up
    signup_response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    assert signup_response.status_code == 200
    
    # Verify signed up
    get_response = client.get("/activities")
    assert email in get_response.json()[activity]["participants"]
    
    # Unregister
    unregister_response = client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    assert unregister_response.status_code == 200
    
    # Verify unregistered
    get_response = client.get("/activities")
    assert email not in get_response.json()[activity]["participants"]


def test_multiple_signups_and_unregisters(client, sample_data):
    """Test complex workflow with multiple students."""
    activity = sample_data["activities"]["empty"]
    email1 = sample_data["emails"]["student1"]
    email2 = sample_data["emails"]["student2"]
    email3 = sample_data["emails"]["student3"]
    
    # Signup three students
    for email in [email1, email2, email3]:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
    
    # Verify all three are signed up
    get_response = client.get("/activities")
    participants = get_response.json()[activity]["participants"]
    assert len(participants) == 3
    assert email1 in participants
    assert email2 in participants
    assert email3 in participants
    
    # Unregister middle student
    response = client.delete(f"/activities/{activity}/unregister?email={email2}")
    assert response.status_code == 200
    
    # Verify correct student was removed
    get_response = client.get("/activities")
    participants = get_response.json()[activity]["participants"]
    assert len(participants) == 2
    assert email1 in participants
    assert email2 not in participants
    assert email3 in participants


def test_signup_duplicate_error_doesnt_affect_list(client, sample_data):
    """Test that failed duplicate signup doesn't corrupt the participants list."""
    activity = sample_data["activities"]["empty"]
    email = sample_data["emails"]["student1"]
    
    # First signup succeeds
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response1.status_code == 200
    
    # Second signup fails
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    
    # Verify participant list is correct (student appears only once)
    get_response = client.get("/activities")
    participants = get_response.json()[activity]["participants"]
    assert participants.count(email) == 1


def test_signup_unregister_multiple_activities(client, sample_data):
    """Test signup and unregister across different activities."""
    activity1 = sample_data["activities"]["empty"]
    activity2 = sample_data["activities"]["with_participants"]
    email = sample_data["emails"]["student1"]
    
    # Sign up for first activity
    response = client.post(f"/activities/{activity1}/signup?email={email}")
    assert response.status_code == 200
    
    # Sign up for second activity
    response = client.post(f"/activities/{activity2}/signup?email={email}")
    assert response.status_code == 200
    
    # Verify in both
    get_response = client.get("/activities")
    assert email in get_response.json()[activity1]["participants"]
    assert email in get_response.json()[activity2]["participants"]
    
    # Unregister from first
    response = client.delete(f"/activities/{activity1}/unregister?email={email}")
    assert response.status_code == 200
    
    # Verify in second but not first
    get_response = client.get("/activities")
    assert email not in get_response.json()[activity1]["participants"]
    assert email in get_response.json()[activity2]["participants"]
