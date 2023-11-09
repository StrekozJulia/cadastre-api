FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
WORKDIR /app
COPY ./cadastre/ /app
COPY ./requirements.txt /app/requirements.txt
COPY ./.env /app/.env
RUN pip install --no-cache-dir --upgrade -r requirements.txt
