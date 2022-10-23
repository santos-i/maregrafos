from typing import List, Union

from pydantic import BaseModel


class TideDataBase(BaseModel):
    timeStamp: int
    temp: float
    nivel: float


class TideDataCreate(TideDataBase):
    pass


class Tide(TideDataBase):
    id: int
    tideGauge_id: int

    class Config:
        orm_mode = True


class TideGaugeBase(BaseModel):
    name: str
    lat: float
    lon: float


class TideGaugeCreate(TideGaugeBase):
    pass


class TideGauge(TideGaugeBase):
    id: int
    name: str
    lat: float
    lon: float

    class Config:
        orm_mode = True