"""Pytest configuration and fixtures for FastAPI tests."""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provide a TestClient instance with a clean state for each test."""
    # Reset the activities to a known state before each test
    from src import app as app_module
    
    # Store original activities
    original_activities = app_module.activities.copy()
    
    # Create a deep copy for this test with reset participants
    app_module.activities = {
        name: {
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "participants": details["participants"].copy()
        }
        for name, details in original_activities.items()
    }
    
    # Create client
    test_client = TestClient(app)
    
    yield test_client
    
    # Restore after test
    app_module.activities = original_activities


@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {
        "emails": {
            "student1": "student1@mergington.edu",
            "student2": "student2@mergington.edu",
            "student3": "student3@mergington.edu",
        },
        "activities": {
            "empty": "Basketball Team",
            "with_participants": "Chess Club",
            "full": "Gym Class",
        }
    }
