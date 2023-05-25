from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_meeting_room_exists, \
    check_reservation_intersections, \
    check_reservation_before_edit
from app.core.db import get_async_session
from app.crud.reservation import reservation_crud
from app.schemas.reservation import ReservationDB, ReservationCreate, \
    ReservationUpdate

router = APIRouter()


@router.post(
    '/',
    # схема ответа, после создания объекта в БД
    response_model=ReservationDB,
)
async def create_reservation(
        reservation: ReservationCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await check_meeting_room_exists(
        reservation.meetingroom_id, session
    )
    await check_reservation_intersections(
        # Так как валидатор принимает **kwargs,
        # аргументы должны быть переданы с указанием ключей.
        **reservation.dict(), session=session
    )
    new_reservation = await reservation_crud.create(
        reservation, session
    )
    return new_reservation


@router.get(
    '/',
    response_model=list[ReservationDB]
)
async def get_all_reservations(
        session: AsyncSession = Depends(get_async_session)
):
    reservations = await reservation_crud.get_multi(session)
    return reservations


@router.delete(
    '/{reservation_id}',
    response_model=ReservationDB
)
async def delete_reservation(
        reservation_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    reservation = await check_reservation_before_edit(reservation_id, session)
    reservation = await reservation_crud.remove(reservation, session)
    return reservation

@router.patch(
    '/{reservation_id}',
    response_model=ReservationDB
)
async def update_reservation(
        reservation_id: int,
        data_in: ReservationUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    # валидируем существование такой брони
    reservation = await check_reservation_before_edit(reservation_id, session)
    # проверяем отсутствие пересечений новых данных
    await check_reservation_intersections(
        **data_in.dict(),
        reservation_id=reservation_id,
        meetingroom_id=reservation.meetingroom_id,
        session=session
    )
    # обновляем данные базовым CRUD-методом
    reservation = await reservation_crud.update(
        db_obj=reservation,
        obj_in=data_in,
        session=session)
    return reservation
