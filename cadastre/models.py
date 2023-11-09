from sqlalchemy import (Column,
                        Integer,
                        String,
                        Boolean,
                        DateTime)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class QueryModel(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    cadastre_num = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    created_at = Column(DateTime)
    answer = Column(Boolean)
