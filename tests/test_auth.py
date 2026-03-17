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

def test_login_success(client, test_user):
    login_payload = {
        "username": "lucas@example.com",
        "password": "test1234"
    }

    response = client.post("/auth/token", data=login_payload)

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_fail(client, test_user):
    login_payload = {
        "username": "lucas@example.com",
        "password": "wrontpassword"
    }
    response = client.post("/auth/token", data=login_payload)

    assert response.status_code == 401