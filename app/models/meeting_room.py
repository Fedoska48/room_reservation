from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class MeetingRoom(Base):
    """Модель переговорок."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    # обратная взаимосвязь с моделью Reservation
    # каскадное удаление связанных резерваций, при удалении комнаты
    reservations = relationship('Reservation', cascade='delete')
