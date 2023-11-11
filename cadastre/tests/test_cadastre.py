import json
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient

from cadastre.main import app

client = TestClient(app)


@patch('cadastre.cadastre.get_remote')
def test_ping_cadastre_ok(mock_get):
    mock_get.return_value = Mock(ok=True)
    response = client.get('/cadastre/ping')
    assert response.status_code == 200
    assert response.json() == 'Сервер доступен'


@patch('cadastre.cadastre.get_remote')
def test_ping_cadastre_not_ok(mock_get):
    mock_get.return_value = Mock(ok=False)
    response = client.get('/cadastre/ping')
    assert response.status_code == 200
    assert response.json() == 'Сервер недоступен'


@patch('cadastre.cadastre.post_remote')
def test_get_answer_cadastre_ok(mock_post):
    result = {"result": True}
    request = json.dumps({
            "cadastre_num": "47:14:1203001:814",
            "latitude": "+18.65",
            "longitude": "-56.658"
        })

    mock_post.return_value = Mock(ok=True)
    mock_post.return_value.json.return_value = result
    response = client.post('/cadastre/query', data=request)
    assert response.status_code == 200
    assert response.json() is True
    assert '/cadastre/result/' in str(response.url)


@patch('cadastre.cadastre.post_remote')
@patch('cadastre.cadastre.get_remote')
def test_get_answer_cadastre_not_ok(mock_post, mock_get):
    request = json.dumps({
            "cadastre_num": "47:14:1203001:814",
            "latitude": "+18.65",
            "longitude": "-56.658"
        })

    mock_post.return_value = Mock(ok=False)
    mock_get.return_value = Mock(ok=False)
    response = client.post('/cadastre/query', data=request)
    assert response.status_code == 200
    assert response.json() == 'Сервер недоступен'
    assert '/cadastre/ping' in str(response.url)
