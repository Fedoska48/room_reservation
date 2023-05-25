# валидаторы
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.models import MeetingRoom, Reservation


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


async def check_reservation_intersections(**kwargs) -> None:
    """Проверка пересечений по бронированию."""
    reservations = await reservation_crud.get_reservations_at_the_same_time(
        **kwargs
    )
    if reservations:
        raise HTTPException(
            status_code=422,
            detail=str(reservations)
        )


async def check_reservation_before_edit(
        reservation_id: int,
        session: AsyncSession
) -> Reservation:
    """Проверка существования объекта в БД"""
    # идем в БД за объектом для изменений
    reservation = await reservation_crud.get(reservation_id, session)
    # обрабатываем ситуацию, когда требуемой переговорки нет
    if not reservation:
        raise HTTPException(
            status_code=404,
            detail='Бронь не найдена!'
        )
    return reservation
