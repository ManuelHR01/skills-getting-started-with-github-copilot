
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

client = TestClient(app)

# Estado original de activities para restaurar antes de cada test
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)

@pytest.fixture(autouse=True)
def restore_activities():
    # Limpiar y restaurar el estado original antes de cada prueba
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))

# AAA: Arrange-Act-Assert

def test_get_activities():
    # Arrange: Nada que preparar, solo el cliente
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "nuevo@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Cleanup: eliminar el participante para no afectar otras pruebas
    client.post(f"/activities/{activity}/unregister", json={"email": email})


def test_signup_already_registered():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Ya está inscrito por defecto
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "ya está inscrito" in response.json()["detail"]


def test_signup_activity_not_found():
    # Arrange
    activity = "NoExiste"
    email = "alguien@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success():
    # Arrange
    activity = "Chess Club"
    email = "tempdelete@mergington.edu"
    # Primero inscribir para poder eliminar
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]


def test_unregister_not_found():
    # Arrange
    activity = "Chess Club"
    email = "noexiste@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_unregister_activity_not_found():
    # Arrange
    activity = "NoExiste"
    email = "alguien@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
