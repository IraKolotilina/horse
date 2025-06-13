import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)




client = TestClient(app)


def generate_name(prefix="building"):
    return f"{prefix}_{uuid.uuid4().hex[:4]}"


@pytest.fixture(scope="module")
def user_credentials():
    suffix = uuid.uuid4().hex[:6]
    return {
        "username": f"user_{suffix}",
        "email": f"{suffix}@example.com",
        "password": "securepass"
    }


@pytest.fixture(scope="module")
def auth_headers(user_credentials):
    client.post("/players/", json=user_credentials)
    response = client.post(
        "/auth/login",
        data={
            "username": user_credentials["username"],
            "password": user_credentials["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture(scope="module")
def stable_id(auth_headers):
    response = client.post("/stables/", json={"name": generate_name("stable")}, headers=auth_headers)
    assert response.status_code == 200
    return response.json()["id"]


def test_create_building(auth_headers, stable_id):
    payload = {"type": "track", "level": 1}
    response = client.post(f"/stables/{stable_id}/buildings", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == payload["type"]
    assert data["level"] == payload["level"]


def test_upgrade_building(auth_headers, stable_id):
    # Повышаем stable до уровня 2
    upgrade_stable = {"type": "stable", "level": 2}
    resp = client.post(
        f"/stables/{stable_id}/buildings",
        json=upgrade_stable,
        headers=auth_headers
    )
    assert resp.status_code == 200

    # Теперь можно повысить track до 2
    payload = {"type": "track", "level": 2}
    response = client.post(f"/stables/{stable_id}/buildings", json=payload, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["level"] == 2


def test_building_cannot_exceed_stable_level(auth_headers, stable_id):
    payload = {"type": "arena", "level": 99}
    response = client.post(f"/stables/{stable_id}/buildings", json=payload, headers=auth_headers)
    assert response.status_code == 400
    assert "stable level" in response.text


def test_stable_upgrade_above_5_requires_all_buildings_level_5(auth_headers, stable_id):
    # Повысим stable до 5 (понадобится для создания зданий 5 уровня)
    resp = client.post(
        f"/stables/{stable_id}/buildings",
        json={"type": "stable", "level": 5},
        headers=auth_headers
    )
    assert resp.status_code == 200

    building_types = [
        "garage", "shop", "warehouse", "vet_box",
        "track", "arena", "plaza", "race_track"
    ]
    # Создаем все здания уровня 5
    for btype in building_types:
        response = client.post(
            f"/stables/{stable_id}/buildings",
            json={"type": btype, "level": 5},
            headers=auth_headers
        )
        assert response.status_code == 200

    # Теперь можно повысить stable до 6 (через stable или administration — выбери то, что реализовано)
    response = client.post(
        f"/stables/{stable_id}/buildings",
        json={"type": "stable", "level": 6},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["level"] == 6
