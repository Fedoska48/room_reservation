from sqlalchemy import Column, DateTime, ForeignKey, Integer

from app.core.db import Base


class Reservation(Base):
    """Модель бронирования."""
    meetingroom_id = Column(Integer, ForeignKey('meetingroom.id'))
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
