import time
from fastapi import FastAPI, status, Body
from random import choice


server = FastAPI()


@server.get('/ping')
def ping():
    """Отклик удаленного сервера на get-запрос"""
    return status.HTTP_200_OK


@server.post('/get_answer')
def get_answer(request=Body()):
    """Отклик удаленного сервера на post-запрос"""
    if (
        request['cadastre_num'] and
        request['latitude'] and
        request['longitude']
    ):
        time.sleep(choice(range(61)))
        return {"result": choice([True, False])}
    return status.HTTP_400_BAD_REQUEST
