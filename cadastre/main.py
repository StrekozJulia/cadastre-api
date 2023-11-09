import uvicorn
import requests
import time
from random import choice
import starlette.status as status

from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from sqladmin import Admin
from typing import Optional
from unittest.mock import patch, Mock

from database import db, engine
from models import QueryModel, Base
from schemas import QuerySchema
from admin import QueryAdmin

SERVER_STATUS_OK = True

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_answer(request=None):
    """
    Функция запроса к удаленному серверу.
    При наличии данных отправляется post-запрос.
    При их отсутствии при помощи get проверяется доступность сервера.
    """
    if request:
        response = requests.post(
                'https://get_answer.com',
                request
            )
    else:
        response = requests.get(
                'https://get_answer.com'
            )
    return response


@patch('requests.post')
@patch('requests.get')
def mock_get_answer(mock_get, mock_post, request=None,):
    """
    Функция-обманка для эмуляции запроса к серверу
    """
    result = {"result": choice([True, False])}
    mock_post.return_value = Mock(ok=SERVER_STATUS_OK)
    mock_post.return_value.json.return_value = result
    mock_get.return_value = Mock(ok=SERVER_STATUS_OK)
    response = get_answer(request)
    if request:
        # Имитация выполнения запроса длительностью до 60 секунд
        time.sleep(choice(range(61)))
    return response


def add_query(data):
    """
    Принимает данные запроса и ответ.
    Сохраняет запрос с результатами в базу данных.
    """
    query = QueryModel(cadastre_num=data['cadastre_num'],
                       latitude=data['latitude'],
                       longitude=data['longitude'],
                       created_at=datetime.now(),
                       answer=data['answer'])
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


@app.get("/ping")
def ping():
    """Проверка доступности удаленного сервера"""
    response = mock_get_answer()
    if response.ok:
        return "Сервер доступен"
    return "Сервер недоступен"


@app.post("/query")
def query(query: QuerySchema):
    """Запрос на удаленный сервер с записью в БД"""
    data = {
            "cadastre_num": query.cadastre_num,
            "latitude": query.latitude,
            "longitude": query.longitude
        }
    response = mock_get_answer(request=data)
    if not response.ok:
        return RedirectResponse(
            "/ping",
            status_code=status.HTTP_302_FOUND
        )
    data["answer"] = mock_get_answer(request=data).json()['result']
    result = add_query(data)
    return RedirectResponse(
        f"/result/{result.id}",
        status_code=status.HTTP_302_FOUND
    )


@app.get("/result/{result_id}")
def result(result_id):
    """Выдача результатов запроса на удаленный сервер"""
    query = db.query(QueryModel).filter(QueryModel.id == result_id).first()
    return query.answer


@app.get("/history")
def history(cadastre_num: Optional[str] = None):
    """История запросов с возможностью фильтрации по кадастровому номеру"""
    result = db.query(QueryModel)
    if cadastre_num:
        return result.filter(QueryModel.cadastre_num == cadastre_num).all()
    return result.all()


# Регистрация админ-панели
admin = Admin(app, engine)
admin.add_view(QueryAdmin)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
