from fastapi.testclient import TestClient

from cadastre.main import app

client = TestClient(app)


def test_ping_server():
    """
    Тестирование отклика удаленного сервера
    """
    response = client.get("/server/ping/")
    assert response.status_code == 200


def test_get_answer_server_data():
    """
    Тестирование ответа на post-запрос к удаленному
    серверу при передаче полных данных в запросе
    """
    request = {
            "cadastre_num": "cadastre_num",
            "latitude": "latitude",
            "longitude": "longitude"
        }
    response = client.post("/server/get_answer/", json=request)
    assert response.status_code == 200
    assert response.json() in (
        {"result": True},
        {"result": False}
    )


def test_get_answer_server_no_data():
    """
    Тестирование ответа на post-запрос к удаленному
    серверу при передаче неполных данных в запросе
    """
    request = {
            "cadastre_num": None,
            "latitude": None,
            "longitude": None
        }
    response = client.post("/server/get_answer/", json=request)
    assert response.status_code == 200
