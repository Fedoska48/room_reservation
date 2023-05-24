from datetime import datetime

from pydantic import BaseModel, validator, root_validator


# базовая схема
class ReservationBase(BaseModel):
    from_reserve: datetime
    to_reserve: datetime


# схема для обновления
class ReservationUpdate(ReservationBase):

    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value):
        if value <= datetime.now():
            raise ValueError('Время начала должно быть раньше текущего!')
        return value

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if values['from_reverse'] >= values['to_reverse']:
            raise ValueError('Время начала должно быть раньше окончания!')
        return values


# схема для создания
class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


# схема для возврата данных
class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int

    class Config:
        # для того, чтобы можно было сериализовать объекты ORM,
        # а не только Python-словарь или JSON
        orm_mode = True
