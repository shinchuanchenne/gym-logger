def test_create_workout(client, auth_headers):
    payload = {
        "title": "Push Day",
        "workout_date": "2026-03-13",
        "notes": "chest and shoulders"
    }

    response = client.post("/workouts", json=payload, headers=auth_headers)

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Push Day"
    assert data["workout_date"] == "2026-03-13"
    assert data["notes"] == "chest and shoulders"
    assert "id" in data
    assert "user_id" in data
    assert "created_at" in data

def test_cannot_access_another_useer_workout(client, auth_headers, another_auth_headers):
    created_payload = {
        "title": "Leg Day",
        "workout_date": "2026-03-25",
        "notes": "squat day"
    }
    create_response = client.post("/workouts", json=created_payload, headers=auth_headers)
    workout_id = create_response.json()["id"]

    response = client.get(f"/workouts/{workout_id}", headers=another_auth_headers)

    assert response.status_code in (403, 404)

def test_get_workout_wrong_id_returns_404(client, auth_headers):
    response = client.get("/workouts/999999", headers=auth_headers)
    assert response.status_code == 404