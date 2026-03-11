def test_login_success(client):
    # Create user
    client.post("/users", json={
        "username": "authuser",
        "email": "auth@example.com",
        "password": "StrongPass123"
    })

    # Login
    response = client.post(
        "/auth/login",
        data={
            "username": "authuser",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/users", json={
        "username": "wronguser",
        "email": "wrong@example.com",
        "password": "StrongPass123"
    })

    response = client.post(
        "/auth/login",
        data={
            "username": "wronguser",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401

def test_login_invalid_user(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "nouser",
            "password": "password"
        }
    )

    assert response.status_code == 401