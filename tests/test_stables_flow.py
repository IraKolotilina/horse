import uuid
import pytest
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

    horse_data = {
        "name": generate_unique_name("horse"),
        "gender": "female",
        "breed": "arabian",
        "speed": 10.0,
        "stamina": 8.0,
        "strength": 9.0,
        "stable_id": stable_id  # <-- UUID как строка
    }

    horse = client.post("/horses/", json=horse_data, headers=auth_headers)
    assert horse.status_code == 200
    assert horse.json()["name"] == horse_data["name"]
    assert horse.json()["stable_id"] == stable_id
