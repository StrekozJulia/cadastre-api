import json
from datetime import datetime
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from cadastre.database import engine, SessionLocal
from cadastre.main import app
from cadastre.models import Base, QueryModel

client = TestClient(app)


class TestQuery:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = SessionLocal()

    def teardown_class(self):
        self.session.rollback()
        self.session.close()
        Base.metadata.drop_all(engine)

    @patch('cadastre.cadastre.get_remote')
    def test_ping_server_ok(self, mock_get):
        """
        Тестирование отклика эндпоинта /ping в случае
        доступности удаленного сервера 
        """
        mock_get.return_value = Mock(ok=True)
        response = client.get('/cadastre/ping')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == 'Сервер доступен'

    @patch('cadastre.cadastre.get_remote')
    def test_ping_server_not_ok(self, mock_get):
        """
        Тестирование отклика эндпоинта /ping в случае
        недоступности удаленного сервера 
        """
        mock_get.return_value = Mock(ok=False)
        response = client.get('/cadastre/ping')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == 'Сервер недоступен'

    @patch('cadastre.cadastre.post_remote')
    @patch('cadastre.cadastre.get_remote')
    def test_query_server_not_ok(self, mock_post, mock_get):
        """
        Тестирование отклика эндпоинта /query в случае
        доступности внешнего сервера
        """
        request = json.dumps({
                "cadastre_num": "47:14:1203001:814",
                "latitude": "+18.65",
                "longitude": "-56.658"
            })

        mock_post.return_value = Mock(ok=False)
        mock_get.return_value = Mock(ok=False)
        response = client.post('/cadastre/query', data=request)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == 'Сервер недоступен'
        assert '/cadastre/ping' in str(response.url)

    @patch('cadastre.cadastre.post_remote')
    def test_get_answer_cadastre_ok(self, mock_post_remote):
        """
        Тестирование отклика эндпоинта /query в случае
        недоступности внешнего сервера
        """
        result = {"result": True}
        request = json.dumps({
                "cadastre_num": "47:14:1203001:814",
                "latitude": "+18.65",
                "longitude": "-56.658"
            })
        mock_post_remote.return_value = Mock(ok=True)
        mock_post_remote.return_value.json.return_value = result
        response = client.post('/cadastre/query', data=request)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is True
        assert '/cadastre/result/1' in str(response.url)

    def test_result(self):
        """
        Тестирование отклика эндпоинта /result
        """
        response = client.get('/cadastre/result/1')
        query = self.session.query(QueryModel).filter_by(id=1).first()
        assert response.json() == query.answer

    def test_history(self):
        """
        Тестирование отклика эндпоинта /history
        """
        self.session.add(QueryModel(
            cadastre_num="47:14:1203001:814",
            latitude="+18.65",
            longitude="-56.658",
            created_at=datetime.now(),
            answer=True
        ))
        self.session.add(QueryModel(
            cadastre_num="47:14:1203001:815",
            latitude="-18.65",
            longitude="+56.658",
            created_at=datetime.now(),
            answer=True
        ))
        self.session.commit()

        response1 = client.get('/cadastre/history')
        response2 = client.get(
            '/cadastre/history?cadastre_num=47:14:1203001:814'
        )
        queryset1 = self.session.query(QueryModel).all()
        queryset2 = self.session.query(QueryModel).filter_by(
            cadastre_num="47:14:1203001:814"
        ).all()
        assert response1.status_code == status.HTTP_200_OK
        assert len(response1.json()) == len(queryset1)
        assert response2.status_code == status.HTTP_200_OK
        assert len(response2.json()) == len(queryset2)
