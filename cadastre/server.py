import time
from fastapi import FastAPI, status, Body
from random import choice


server = FastAPI()


@server.get('/ping')
def ping():
    return status.HTTP_200_OK


@server.post('/get_answer')
def get_answer(request=Body()):
    if (
        request['cadastre_num'] and
        request['latitude'] and
        request['longitude']
    ):
        time.sleep(choice(range(61)))
        return {"result": choice([True, False])}
    return status.HTTP_400_BAD_REQUEST
