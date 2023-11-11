from pydantic import BaseModel, Field, field_validator

from .constants import (CADASTRE_REGEX,
                        LATITUDE_REGEX,
                        LONGITUDE_REGEX)


class QuerySchema(BaseModel):
    cadastre_num: str = Field(pattern=CADASTRE_REGEX)
    latitude: str = Field(pattern=LATITUDE_REGEX)
    longitude: str = Field(pattern=LONGITUDE_REGEX)

    @field_validator('latitude')
    def latitude_validator(cls, value: str):
        """Проверяем, что значение широты в пределах +-90 градусов"""
        if value[0] in ('+-'):
            float_value = float(value[1:])
        else:
            float_value = float(value)
        if float_value > 90.0:
            raise ValueError('Latitude should get value between -90 and +90')
        return value

    @field_validator('longitude')
    def longitude_validator(cls, value: str):
        """Проверяем, что значение долготы в пределах +-180 градусов"""
        if value[0] in ('+-'):
            float_value = float(value[1:])
        else:
            float_value = float(value)
        if float_value > 180.0:
            raise ValueError(
                'Longitude should get value between -180 and +180'
            )
        return value
