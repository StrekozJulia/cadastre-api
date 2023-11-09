# import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv("../.env")
# print(os.environ)

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db" # os.environ["DB_URL"]

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
