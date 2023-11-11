FROM python:3.11
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY ./sql_app.db /app/sql_app.db
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./cadastre/ /app/cadastre/
CMD ["uvicorn", "cadastre.main:app", "--host", "0.0.0.0", "--port", "80"]
