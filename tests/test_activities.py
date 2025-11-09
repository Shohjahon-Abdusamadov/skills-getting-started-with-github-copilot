import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic sanity checks
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    act = "Basketball Team"
    email = "pytest-tester@example.com"

    # Ensure clean state: try to unregister if present
    client.delete(f"/activities/{act}/unregister?email={email}")

    # Sign up
    resp = client.post(f"/activities/{act}/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant appears
    resp = client.get("/activities")
    assert resp.status_code == 200
    participants = resp.json()[act]["participants"]
    assert email in participants

    # Duplicate signup should return 400
    resp = client.post(f"/activities/{act}/signup?email={email}")
    assert resp.status_code == 400

    # Unregister
    resp = client.delete(f"/activities/{act}/unregister?email={email}")
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")

    # Verify removed
    resp = client.get("/activities")
    participants = resp.json()[act]["participants"]
    assert email not in participants
