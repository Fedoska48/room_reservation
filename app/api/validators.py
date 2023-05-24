# валидаторы
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.models import MeetingRoom


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession
) -> None:
    """Проверка Названия переговорки на уникальность"""
    room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!'
        )
    return room_id


async def check_meeting_room_exists(
        meeting_room_id: int,
        session: AsyncSession
) -> MeetingRoom:
    """Проверка существования объекта в БД"""
    # идем в БД за объектом для изменений
    meeting_room = await meeting_room_crud.get(meeting_room_id, session)
    # обрабатываем ситуацию, когда требуемой переговорки нет
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return meeting_room
