"""Создадим в проекте отдельные Pydantic-модели для разных эндпоинтов:
в одной будет одно обязательное и одно опциональное поле,
в другой — только опциональные."""
from typing import Optional

from pydantic import BaseModel, Field, validator


class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


# схема для создания объекта переговорки
class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(..., min_length=1, max_length=100)


# класс для обновления объектов.
class MeetingRoomUpdate(MeetingRoomBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Поле name явялется обязательным')
        return value


# схема для возврата более красивых данных из БД
class MeetingRoomBD(MeetingRoomCreate):
    id: int

    class Config:
        # для того, чтобы можно было сериализовать объекты ORM,
        # а не только Python-словарь или JSON
        orm_mode = True
