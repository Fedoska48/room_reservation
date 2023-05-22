# функции непосредственно взаимодействующие с БД
from typing import Optional, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import AsyncSessionLocal
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


# функция принимает Pydantic-модель, а возвращает ORM-модель
async def create_meeting_room(
        new_room: MeetingRoomCreate,
        session: AsyncSession
) -> MeetingRoom:
    """Создание переговорки."""

    # конвертация MeetingRoomCreate в словарь
    new_room_data = new_room.dict()

    # создаем объект модели MeetingRoom
    # В параметры передаём пары "ключ=значение",для этого распаковываем словарь
    db_room = MeetingRoom(**new_room_data)

    # сессия уже создана асинх.генератором и передается вторым параметром
    # добавляем объект в сессию
    session.add(db_room)
    # записываем данные в БД
    await session.commit()
    # Обновляем объект db_room:считываем данные из БД,чтобы получить его id
    await session.refresh(db_room)
    # Возвращаем только что созданный объект класса MeetingRoom.
    return db_room


async def get_room_id_by_name(
        # прнимаем название преговорки
        room_name: str,
        session: AsyncSession
) -> Optional[int]:  # может вернуть ID, либо ничего (если нет такой)
    """Получить ID переговорки на основе Названия."""

    # сессия уже создана асинх.генератором и передается вторым параметром
    # делаем запрос к БД на получение объекта (объект Result)
    db_room_id = await session.execute(
        select(MeetingRoom.id).where(MeetingRoom.name == room_name)
    )
    # извлекаем данные из объекта
    db_room_id = db_room_id.scalars().first()
    return db_room_id


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession
) -> None:
    """Проверка Названия переговорки на уникальность"""
    room_id = await get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!'
        )
    return room_id


async def read_all_rooms_from_db(session: AsyncSession) -> list[MeetingRoom]:
    """Получение списка всех переговорок"""
    # делаем запрос к БД на получение объектов
    db_rooms = await session.execute(select(MeetingRoom))
    # извлекаем данные и возращаем
    return db_rooms.scalars().all()


async def get_meeting_room_by_id(
        # прнимаем ID преговорки
        room_id: int,
        session: AsyncSession
) -> Optional[MeetingRoom]:
    """Получить объект переговорки на основе ID."""

    # сессия уже создана асинх.генератором и передается вторым параметром
    # делаем запрос к БД на получение объекта (объект Result)
    db_room = await session.execute(
        select(MeetingRoom).where(MeetingRoom.id == room_id)
    )
    # извлекаем данные из объекта
    db_room = db_room.scalars().first()
    return db_room


async def update_meeting_room(
        # объект из БД для обновления
        db_room: MeetingRoom,
        # данные из запроса, которые необходимо внести в БД
        room_in: MeetingRoomUpdate,
        # асинхронная сессия
        session: AsyncSession
) -> MeetingRoom:
    # декодируем объект из БД в словарь
    obj_data = jsonable_encoder(db_room)
    # Конвертируем объект с данными из запроса в словарь
    # исключаем неустановленные значения
    update_data = room_in.dict(exclude_unset=True)

    # перебираем ключи объекта-словаря из БД
    for field in obj_data:
        # проверяем наличие полей БД во входных данных
        if field in update_data:
            # устанавливаем новые значения в полях
            setattr(db_room, field, update_data[field])
    # добавляем новое значение в сессию
    session.add(db_room)
    # подтверждаем изменения
    await session.commit()
    # обновляем объект из БД
    await session.refresh(db_room)
    return db_room


async def delete_meeting_room(
        # объект из БД для удаления
        db_room: MeetingRoom,
        # асинхронная сессия
        session: AsyncSession
) -> MeetingRoom:
    """Удаление объекта переговорки"""
    await session.delete(db_room)
    await session.commit()
    # не делаем refresh => еще содержится информация об объекте, ее возвращаем
    return db_room


async def check_meeting_room_exists(
        meeting_room_id: int,
        session: AsyncSession):
    """Проверка существования объекта в БД"""
    # идем в БД за объектом для изменений
    meeting_room = await get_meeting_room_by_id(meeting_room_id, session)
    # обрабатываем ситуацию, когда требуемой переговорки нет
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return meeting_room
