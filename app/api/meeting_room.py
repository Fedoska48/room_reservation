from fastapi import APIRouter, HTTPException

from app.crud.meeting_room import create_meeting_room, get_room_id_by_name
from app.schemas.meeting_room import MeetingRoomCreate

router = APIRouter()


@router.post('/meeting_room/')  # закрывающий слеш т.к. будет раширение
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate  # Валидация по MeetingRoomCreate
):
    """Описываем эндпойнт - верхнеуровнево шаги.
    Сама логика занесения в БД - в разделе CRUD"""

    # обработка дублей на уровне кода
    room_id = await get_room_id_by_name(meeting_room.name)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!'
        )

    # вызов корутины по созданию объекта
    new_room = await create_meeting_room(meeting_room)
    return new_room
