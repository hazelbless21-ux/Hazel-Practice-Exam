from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_participant():
    activity = "Chess Club"
    email = "test.student@mergington.edu"

    # Ensure participant is not present initially (if present, remove it first)
    resp = client.get(f"/activities")
    assert resp.status_code == 200
    activities = resp.json()
    participants = activities[activity].get("participants", [])
    if email in participants:
        del_resp = client.delete(f"/activities/{activity}/participants?email={email}")
        assert del_resp.status_code in (200, 404)

    # Sign up the participant
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    signup_json = signup_resp.json()
    assert "Signed up" in signup_json.get("message", "")

    # Verify participant appears in the activity
    resp_after = client.get(f"/activities")
    assert resp_after.status_code == 200
    activities_after = resp_after.json()
    assert email in activities_after[activity]["participants"]

    # Unregister participant
    del_resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert del_resp.status_code == 200
    del_json = del_resp.json()
    assert "Removed" in del_json.get("message", "")

    # Verify participant removed
    resp_final = client.get(f"/activities")
    assert resp_final.status_code == 200
    activities_final = resp_final.json()
    assert email not in activities_final[activity]["participants"]
