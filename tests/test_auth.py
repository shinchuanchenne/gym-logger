def test_app_exists(client):
    assert client is not None

def test_register_success(client):
    payload = {
        "username": "lucas",
        "email": "lucas@example.com",
        "password": "test1234"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["username"] == "lucas"
    assert data["email"] == "lucas@example.com"
    assert "id" in data
    assert "created_at" in data