import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def user_credentials():
    suffix = uuid.uuid4().hex[:6]
    return {
        "username": f"horse_tester_{suffix}",
        "email": f"horse_{suffix}@example.com",
        "password": "securepass"
    }


@pytest.fixture(scope="module")
def access_token(user_credentials):
    client.post("/players/", json=user_credentials)

    response = client.post(
        "/auth/login",
        data={
            "grant_type": "password",
            "username": user_credentials["username"],
            "password": user_credentials["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def auth_headers(access_token):
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="module")
def stable_id(auth_headers):
    resp = client.post("/stables/", json={"name": f"Stable_{uuid.uuid4().hex[:4]}"}, headers=auth_headers)
    assert resp.status_code == 200
    return resp.json()["id"]


@pytest.fixture(scope="module")
def created_horses(auth_headers, stable_id):
    horses = []
    for i in range(2):
        horse_data = {
            "name": f"Horse_{i}_{uuid.uuid4().hex[:4]}",
            "gender": "female" if i == 0 else "male",
            "breed": "Arabian",
            "speed": 50.0,
            "stamina": 55.0,
            "strength": 60.0,
            "jump": 45.0,
            "height": 160.0,
            "type": "standard",
            "stable_id": stable_id
        }
        resp = client.post("/horses/", json=horse_data, headers=auth_headers)
        assert resp.status_code == 200
        horse = resp.json()
        # 🛠️ Принудительно увеличиваем возраст
        horse_id = horse["id"]
        patch_resp = client.patch(f"/horses/{horse_id}", json={"age": 5}, headers=auth_headers)
        assert patch_resp.status_code == 200
        horses.append(patch_resp.json())
    return horses


def test_create_horse(auth_headers, stable_id):
    horse_data = {
        "name": f"TestHorse_{uuid.uuid4().hex[:4]}",
        "gender": "male",
        "breed": "Thoroughbred",
        "speed": 48.5,
        "stamina": 52.0,
        "strength": 60.2,
        "jump": 40.0,
        "height": 155.0,
        "type": "standard",
        "stable_id": stable_id
    }
    resp = client.post("/horses/", json=horse_data, headers=auth_headers)
    assert resp.status_code == 200
    horse = resp.json()
    assert horse["name"] == horse_data["name"]
    assert horse["gender"] == horse_data["gender"]
    assert horse["breed"] == horse_data["breed"]
    assert horse["speed"] == horse_data["speed"]
    assert horse["stamina"] == horse_data["stamina"]
    assert horse["strength"] == horse_data["strength"]
    assert horse["jump"] == horse_data["jump"]
    assert horse["height"] == horse_data["height"]
    assert horse["type"] == horse_data["type"]
    assert horse["age"] == 0
    assert horse["is_pregnant"] is False
    assert "gene_speed" in horse
    assert "gene_stamina" in horse
    assert "gene_strength" in horse
    assert "gene_jump" in horse


def test_breed_horse(auth_headers, created_horses):
    mother = created_horses[0]
    father = created_horses[1]

    if mother["age"] < 4 or father["age"] < 4:
        pytest.skip("Один из родителей младше 4 лет — невозможно размножение.")

    foal_data = {
        "mother_id": mother["id"],
        "father_id": father["id"],
        "foal_name": f"Foal_{uuid.uuid4().hex[:4]}"
    }
    resp = client.post("/horses/breed", json=foal_data, headers=auth_headers)
    assert resp.status_code == 200, resp.text
    foal = resp.json()
    assert foal["name"] == foal_data["foal_name"]
    assert foal["age"] == 0
    assert foal["type"] in ("standard", "legendary")
    assert "gene_speed" in foal
    assert "gene_stamina" in foal
    assert "gene_strength" in foal
    assert "gene_jump" in foal
    assert isinstance(foal["speed"], float)
    assert isinstance(foal["jump"], float)
    assert foal["is_pregnant"] is False
