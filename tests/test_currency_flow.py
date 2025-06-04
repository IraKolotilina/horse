import uuid
import pytest
from typing import Optional
from app.models.player import Player
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def auth_token():
    # Регистрация нового уникального игрока
    suffix = uuid.uuid4().hex[:6]
    user = {
        "username": f"curr_user_{suffix}",
        "email": f"curr_{suffix}@example.com",
        "password": "securepass"
    }
    resp = client.post("/players/", json=user)
    assert resp.status_code in (200, 409)

    # Логин
    login_resp = client.post(
        "/auth/login",
        data={
            "grant_type": "password",
            "username": user["username"],
            "password": user["password"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_resp.status_code == 200
    return login_resp.json()["access_token"]

def test_get_initial_currency(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = client.get("/players/me/currency", headers=headers)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "real" in data and "game" in data
    assert data["real"] == 0
    assert data["game"] == 0

def test_add_currency(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    update = {"real": 150, "game": 300}
    resp = client.put("/players/me/currency", json=update, headers=headers)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["real"] == 150
    assert data["game"] == 300

def test_spend_currency(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    spend = {"real": -50, "game": -100}
    resp = client.patch("/players/me/currency", json=spend, headers=headers)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["real"] == 100   # 150 - 50
    assert data["game"] == 200   # 300 - 100

def test_overspend_currency(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = client.patch("/players/me/currency", json={"game": -500}, headers=headers)
    assert resp.status_code == 400, "Должна быть ошибка при попытке перерасхода"
