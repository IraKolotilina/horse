import uuid
import pytest
from typing import Optional
from app.models.player import Player
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def generate_unique_name(prefix="entity"):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


@pytest.fixture
def registered_user():
    user = {
        "username": generate_unique_name("user"),
        "email": generate_unique_name("mail") + "@example.com",
        "password": "securepass"
    }
    resp = client.post("/players/", json=user)
    assert resp.status_code in [200, 400]
    return user


@pytest.fixture
def auth_headers(registered_user):
    resp = client.post(
        "/auth/login",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_admin_created_with_stable(auth_headers):
    response = client.post("/stables/", json={"name": generate_unique_name("stable")}, headers=auth_headers)
    assert response.status_code == 200
    stable_id = response.json()["id"]

    buildings = client.get(f"/stables/{stable_id}/buildings", headers=auth_headers)
    assert buildings.status_code == 200
    assert any(b["type"] == "administration" for b in buildings.json())


def test_multiple_stables_have_admin(auth_headers):
    ids = []
    for _ in range(2):
        resp = client.post("/stables/", json={"name": generate_unique_name("stable")}, headers=auth_headers)
        assert resp.status_code == 200
        ids.append(resp.json()["id"])

    for sid in ids:
        buildings = client.get(f"/stables/{sid}/buildings", headers=auth_headers)
        assert buildings.status_code == 200
        assert any(b["type"] == "administration" for b in buildings.json())


def test_level1_stable_has_2_boxes_and_can_create_horse(auth_headers):
    resp = client.post("/stables/", json={"name": generate_unique_name("stable")}, headers=auth_headers)
    assert resp.status_code == 200
    stable_id = resp.json()["id"]

    boxes = client.get(f"/stables/{stable_id}/boxes", headers=auth_headers)
    assert boxes.status_code == 200
    assert len(boxes.json()) == 2

    # Лошадь 1
    horse_data_1 = {
        "name": generate_unique_name("horse1"),
        "gender": "female",
        "breed": "Arabian",
        "speed": 10.0,
        "stamina": 8.0,
        "strength": 9.0,
        "jump": 7.5,
        "height": 160.0,
        "type": "standard",
        "stable_id": stable_id
    }

    horse1 = client.post("/horses/", json=horse_data_1, headers=auth_headers)
    assert horse1.status_code == 200
    h1 = horse1.json()
    assert h1["name"] == horse_data_1["name"]
    assert h1["stable_id"] == stable_id

    # Лошадь 2
    horse_data_2 = {
        "name": generate_unique_name("horse2"),
        "gender": "male",
        "breed": "Arabian",
        "speed": 11.0,
        "stamina": 9.0,
        "strength": 10.0,
        "jump": 8.0,
        "height": 162.0,
        "type": "standard",
        "stable_id": stable_id
    }

    horse2 = client.post("/horses/", json=horse_data_2, headers=auth_headers)
    assert horse2.status_code == 200
    h2 = horse2.json()
    assert h2["name"] == horse_data_2["name"]
    assert h2["stable_id"] == stable_id
