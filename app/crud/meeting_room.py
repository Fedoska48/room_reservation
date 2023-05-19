from typing import Optional

from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate


# функция принимает Pydantic-модель, а возвращает ORM-модель
async def create_meeting_room(
        new_room: MeetingRoomCreate
) -> MeetingRoom:
    """Создание переговорки."""

    # конвертация MeetingRoomCreate в словарь
    new_room_data = new_room.dict()

    # создаем объект модели MeetingRoom
    # В параметры передаём пары "ключ=значение",для этого распаковываем словарь
    db_room = MeetingRoom(**new_room_data)

    # создаем асинхронную сессию через контектсный менеджер
    async with AsyncSessionLocal() as session:
        # добавляем объект в сессию
        session.add(db_room)
        # записываем данные в БД
        await session.commit()
        # Обновляем объект db_room:считываем данные из БД,чтобы получить его id
        await session.refresh(db_room)
    # Возвращаем только что созданный объект класса MeetingRoom.
    return db_room


async def get_room_id_by_name(
        room_name: str  # прнимаем название преговорки
) -> Optional[int]:  # может вернуть ID, либо ничего (если нет такой)
    """Получить ID переговорки на основе Названия."""

    # создаем сессию
    async with AsyncSessionLocal() as session:
        # делаем запрос к БД на получение объекта (объект Result)
        db_room_id = await session.execute(
            select(MeetingRoom.id).where(MeetingRoom.name == room_name)
        )
        # извлекаем данные из объекта
        db_room_id = db_room_id.scalars().first()
    return db_room_id
