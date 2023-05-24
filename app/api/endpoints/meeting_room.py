from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_meeting_room_exists, check_name_duplicate
from app.core.db import get_async_session
from app.crud.meeting_room import meeting_room_crud
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomBD, \
    MeetingRoomUpdate

# объект роутера для эндпойнта
# параметр префикса, который будет подставляться автомтом ко все ручкам
# параметр тега роутера, который автоматом пойдет во все ручки роутера
router = APIRouter()


# эндпойнт для переговорок
# закрывающий слеш т.к. будет раширение
@router.post(
    '/',
    # схема ответа, после создания объекта в БД
    response_model=MeetingRoomBD,
    # исключать из ответа поля со значением None
    response_model_exclude_none=True,
)
async def create_new_meeting_room(
        # Валидация по MeetingRoomCreate
        meeting_room: MeetingRoomCreate,
        # Указываем зависимость, предоставляющую объект сессии.
        session: AsyncSession = Depends(get_async_session)
):
    """Описываем эндпойнт - верхнеуровнево шаги.
    Сама логика занесения в БД - в разделе CRUD"""

    # обработка дублей на уровне кода
    # передаем сессию в CRUD-функцию
    await check_name_duplicate(meeting_room.name, session)

    # вызов корутины по созданию объекта
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.get(
    '/',
    # схема ответа, после создания объекта в БД
    response_model=list[MeetingRoomBD],
    # исключать из ответа поля со значением None
    response_model_exclude_none=True,
)
async def get_all_meeting_rooms(
        # создаем единую сессию через зависимости
        session: AsyncSession = Depends(get_async_session)
):
    # вызываем CRUD-функцию
    all_rooms = await meeting_room_crud.get_multi(session)
    return all_rooms


@router.patch(
    '/{meeting_room_id}',
    # схема ответа, после создания объекта в БД
    response_model=MeetingRoomBD,
    # исключать из ответа поля со значением None
    response_model_exclude_none=True,
)
async def partially_update_meeting_room(
        # ID обновляемого объекта
        meeting_room_id: int,
        # данные переданные для обновления
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    # проверка на существовании комнаты
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    # если name не пустое, проверяем на дубликаты
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    # обновляем объект
    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    # схема ответа, после создания объекта в БД
    response_model=MeetingRoomBD,
    # исключать из ответа поля со значением None
    response_model_exclude_none=True,
)
async def remove_meeting_room(
        # ID обновляемого объекта
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    # проверка на существовании комнаты
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    meeting_room = await meeting_room_crud.remove(meeting_room, session)
    return meeting_room