from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_meeting_room_exists, check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomBD, \
    MeetingRoomUpdate

# объект роутера для эндпойнта
# параметр префикса, который будет подставляться автомтом ко все ручкам
# параметр тега роутера, который автоматом пойдет во все ручки роутера
from app.schemas.reservation import ReservationDB

router = APIRouter()


# эндпойнт для переговорок
# закрывающий слеш т.к. будет раширение
@router.post(
    '/',
    # схема ответа, после создания объекта в БД
    response_model=MeetingRoomBD,
    # исключать из ответа поля со значением None
    response_model_exclude_none=True,
    # ограничение доступа, учитывая что не требуется передвать user в функцию
    # проверка что запрос получен от superuser
    dependencies=[Depends(current_superuser)]
)
# Описываем эндпойнт - верхнеуровнево.
# Сама логика занесения в БД - в разделе CRUD и валидациях
async def create_new_meeting_room(
        # Валидация по MeetingRoomCreate
        meeting_room: MeetingRoomCreate,
        # Указываем зависимость, предоставляющую объект сессии.
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""

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
    # проверка что запрос получен от superuser
    dependencies=[Depends(current_superuser)]
)
async def partially_update_meeting_room(
        # ID обновляемого объекта
        meeting_room_id: int,
        # данные переданные для обновления
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
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
    # проверка что запрос получен от superuser
    dependencies=[Depends(current_superuser)]
)
async def remove_meeting_room(
        # ID обновляемого объекта
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    # проверка на существовании комнаты
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    meeting_room = await meeting_room_crud.remove(meeting_room, session)
    return meeting_room


@router.get(
    '/{meeting_room_id}/reservations',
    response_model=list[ReservationDB]
)
async def get_reservations_for_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    await check_meeting_room_exists(meeting_room_id, session)
    reservs_by_room = await reservation_crud.get_future_reservations_for_room(
        room_id=meeting_room_id, session=session
    )
    return reservs_by_room
