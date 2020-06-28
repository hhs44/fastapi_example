from typing import List

from pydantic import BaseModel
from pydantic.schema import date


class CarBase(BaseModel):
    carno: str
    owner: str


class Car(CarBase):
    class Config:
        orm_mode = True


class RecordBase(BaseModel):
    reason: str
    makedate: date
    punish: str
    dealt: bool


class Record(RecordBase):
    id: int
    car: Car

    class Config:
        orm_mode = True


class Latest(BaseModel):
    count: int
    currpage: int
    nexturl: str
    preurl: str
    records: List[Record]

    class Config:
        orm_mode = True


class Dealt(BaseModel):
    code: int
    msg: str

