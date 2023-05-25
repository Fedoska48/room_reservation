from datetime import datetime, timedelta

from pydantic import BaseModel, validator, root_validator, Extra, Field

FROM_TIME = (
        datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
        datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


# базовая схема
class ReservationBase(BaseModel):
    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)

    class Config:
        # запрет принимать параметры, которые не описаны в схеме
        extra = Extra.forbid


# схема для обновления
class ReservationUpdate(ReservationBase):

    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value):
        if value <= datetime.now():
            raise ValueError('Время начала должно быть раньше текущего!')
        return value

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if values['from_reserve'] >= values['to_reserve']:
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
