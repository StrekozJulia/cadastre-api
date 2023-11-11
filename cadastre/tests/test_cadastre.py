import json
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from datetime import datetime

from cadastre.models import Base, QueryModel
from cadastre.database import SessionLocal, engine
from cadastre.main import app

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
    def test_ping_cadastre_ok(self, mock_get):
        mock_get.return_value = Mock(ok=True)
        response = client.get('/cadastre/ping')
        assert response.status_code == 200
        assert response.json() == 'Сервер доступен'

    @patch('cadastre.cadastre.get_remote')
    def test_ping_cadastre_not_ok(self, mock_get):
        mock_get.return_value = Mock(ok=False)
        response = client.get('/cadastre/ping')
        assert response.status_code == 200
        assert response.json() == 'Сервер недоступен'

    @patch('cadastre.cadastre.post_remote')
    @patch('cadastre.cadastre.get_remote')
    def test_get_answer_cadastre_not_ok(self, mock_post, mock_get):
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

    @patch('cadastre.cadastre.post_remote')
    def test_get_answer_cadastre_ok(self, mock_post_remote):
        result = {"result": True}
        request = json.dumps({
                "cadastre_num": "47:14:1203001:814",
                "latitude": "+18.65",
                "longitude": "-56.658"
            })
        mock_post_remote.return_value = Mock(ok=True)
        mock_post_remote.return_value.json.return_value = result
        response = client.post('/cadastre/query', data=request)
        assert response.status_code == 200
        assert response.json() is True
        assert '/cadastre/result/1' in str(response.url)

    def test_result(self):
        response = client.get('/cadastre/result/1')
        query = self.session.query(QueryModel).filter_by(id=1).first()
        assert response.json() == query.answer

    def test_history(self):
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
        assert response1.status_code == 200
        assert len(response1.json()) == len(queryset1)
        assert response2.status_code == 200
        assert len(response2.json()) == len(queryset2)
