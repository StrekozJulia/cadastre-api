from datetime import datetime
from pydantic import BaseModel, PositiveInt


class QuerySchema(BaseModel):
    # id: int
    cadastre_num: str
    latitude: str
    longitude: str

    # class Config:
    #     from_attributes = True

