def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"].startswith("Learn strategies")
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity(client):
    email = "tester@mergington.edu"
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email in response.json()["message"]

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_remove_participant(client):
    email = "michael@mergington.edu"
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email in response.json()["message"]

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_signup_duplicate_fails(client):
    email = "michael@mergington.edu"
    first_response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )
    assert first_response.status_code == 400
    assert "already signed up" in first_response.json()["detail"]


def test_remove_nonexistent_participant_fails(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
