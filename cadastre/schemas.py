from pydantic import BaseModel, Field, field_validator

cadastre_regex = r'^\d{2}:\d{2}:\d{6,7}:\d+$'
latitude_regex = r'^[+-]?\d{1,2}.\d+$'
longitude_regex = r'^[+-]?1?\d{1,2}.\d+$'


class QuerySchema(BaseModel):
    cadastre_num: str = Field(pattern=cadastre_regex)
    latitude: str = Field(pattern=latitude_regex)
    longitude: str = Field(pattern=longitude_regex)

    @field_validator('latitude')
    def latitude_validator(cls, value: str):
        if value[0] in ('+-'):
            float_value = float(value[1:])
        else:
            float_value = float(value)
        if float_value > 90.0:
            raise ValueError('Latitude should get value between -90 and +90')
        return value

    @field_validator('longitude')
    def longitude_validator(cls, value: str):
        if value[0] in ('+-'):
            float_value = float(value[1:])
        else:
            float_value = float(value)
        if float_value > 180.0:
            raise ValueError(
                'Longitude should get value between -180 and +180'
            )
        return value
