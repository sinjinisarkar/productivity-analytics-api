def test_create_user(client):
    res = client.post("/users", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "StrongPass123"
    })
    assert res.status_code == 201
    body = res.json()
    assert "id" in body
    assert body["email"] == "testuser@example.com"
    assert "password" not in body
    assert "hashed_password" not in body