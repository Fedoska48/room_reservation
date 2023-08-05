from datetime import datetime
from typing import Optional

from sqlalchemy import select, between, or_, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Reservation, User


class CRUDReservation(CRUDBase):

    @staticmethod
    async def get_reservations_at_the_same_time(
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            reservation_id: Optional[int] = None,
            session: AsyncSession,
    ) -> list[Reservation]:
        # дефолтное условие для выборки
        same_time_objs = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        # если указан ID резерва
        if reservation_id is not None:
            # ...то исключаем текущую бронь из выборки,
            # иначе среагирует сама на себя при обновлении
            same_time_objs = same_time_objs.where(
                Reservation.id != reservation_id
            )
        # выполняем запрос
        reservations = await session.execute(same_time_objs)
        reservations = reservations.scalars().all()
        return reservations

    @staticmethod
    async def get_future_reservations_for_room(
            room_id: int,
            session: AsyncSession
    ):
        """Запрос броней конкретной комнаты."""
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return reservations

    @staticmethod
    async def get_by_user(
            user: User,
            session: AsyncSession
    ):
        """Список объектов Reservation связанных с пользователем."""
        reservations = await session.execute(
            select(Reservation).where(Reservation.user_id == user.id)
        )
        reservations = reservations.scalars().all()
        return reservations


    @staticmethod
    async def get_count_res_at_the_same_time(
            from_reserve: datetime,
            to_reserve: datetime,
            session: AsyncSession
    ) -> list[dict[str, int]]:
        reservations = await session.execute(
            # Получаем количество бронирований переговорок за период
            select([Reservation.meetingroom_id,
                    func.count(Reservation.meetingroom_id)]).where(
                Reservation.from_reserve >= from_reserve,
                Reservation.to_reserve <= to_reserve
            ).group_by(Reservation.meetingroom_id)
        )
        reservations = reservations.all()
        return reservations


reservation_crud = CRUDReservation(Reservation)
