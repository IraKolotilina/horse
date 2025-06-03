import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from typing import Optional

client = TestClient(app)

def generate_user():
    suffix = uuid.uuid4().hex[:6]
    return {
        "username": f"testuser_{suffix}",
        "email": f"test_{suffix}@example.com",
        "password": "securepass"
    }

@pytest.fixture(scope="module")
def user_data():
    return generate_user()

@pytest.fixture(scope="module")
def registered_user(user_data):
    response = client.post("/players/", json=user_data)
    assert response.status_code in [200, 400]
    return user_data

@pytest.fixture(scope="module")
def access_token(registered_user):
    response = client.post(
        "/auth/login",
        data={
            "grant_type": "password",
            "username": registered_user["username"],
            "password": registered_user["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

# -------------------- Тесты регистрации --------------------

def test_registration():
    user = generate_user()
    response = client.post("/players/", json=user)
    assert response.status_code == 200
    assert response.json()["username"] == user["username"]

def test_duplicate_registration(registered_user):
    response = client.post("/players/", json=registered_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

# -------------------- Тесты авторизации --------------------

def test_login_success(registered_user):
    response = client.post(
        "/auth/login",
        data={
            "grant_type": "password",
            "username": registered_user["username"],
            "password": registered_user["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_password(registered_user):
    response = client.post(
        "/auth/login",
        data={
            "grant_type": "password",
            "username": registered_user["username"],
            "password": "wrongpass"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401

def test_login_invalid_username():
    response = client.post(
        "/auth/login",
        data={
            "grant_type": "password",
            "username": "nonexistent_user",
            "password": "somepass"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401

# -------------------- Тесты профиля --------------------

def test_get_profile(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/players/me", headers=headers)
    assert response.status_code == 200
    assert "username" in response.json()

def test_get_profile_without_token():
    response = client.get("/players/me")
    assert response.status_code == 401

def test_get_profile_invalid_token():
    headers = {"Authorization": "Bearer invalid.token.value"}
    response = client.get("/players/me", headers=headers)
    assert response.status_code == 401

# -------------------- Тесты обновления --------------------

def test_update_email_only(access_token):
    new_email = f"updated_{uuid.uuid4().hex[:6]}@example.com"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put("/players/me", headers=headers, json={"email": new_email})
    assert response.status_code == 200
    assert response.json()["email"] == new_email

def test_update_password_only(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put("/players/me", headers=headers, json={"password": "newsecurepass2"})
    assert response.status_code == 200

def test_update_with_empty_payload(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put("/players/me", headers=headers, json={})
    assert response.status_code == 200
    
def test_register_existing_user(registered_user):
    response = client.post("/players/", json=registered_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_login_wrong_password(registered_user):
    response = client.post(
        "/auth/login",
        data={
            "grant_type": "password",
            "username": registered_user["username"],
            "password": "wrongpass"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_access_with_invalid_token():
    headers = {"Authorization": "Bearer invalid.token.here"}
    response = client.get("/players/me", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_update_profile(auth_headers):
    new_email = f"updated_{uuid.uuid4().hex[:6]}@example.com"
    new_password = "newsecurepass"

    update_data = {
        "email": new_email,
        "password": new_password
    }

    # Обновляем профиль
    resp = client.put("/players/update", json=update_data, headers=auth_headers)
    assert resp.status_code == 200

    # Пытаемся залогиниться со старым паролем — должен быть отказ
    old_login = client.post(
        "/auth/login",
        data={"username": auth_headers['Authorization'].split()[1], "password": "securepass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert old_login.status_code == 400

    # Логинимся с новым паролем
    login = client.post(
        "/auth/login",
        data={"username": auth_headers['Authorization'].split()[1], "password": new_password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login.status_code == 200


