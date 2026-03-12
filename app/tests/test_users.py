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


def test_get_user(client):
    created = client.post("/users", json={
        "username": "lookupuser",
        "email": "lookup@example.com",
        "password": "StrongPass123"
    }).json()

    res = client.get(f"/users/{created['id']}")

    assert res.status_code == 200
    body = res.json()
    assert body["id"] == created["id"]
    assert body["username"] == "lookupuser"