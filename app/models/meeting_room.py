from sqlalchemy import Column, String, Text

from app.core.db import Base


class MeetingRoom(Base):
    """Модель переговорок."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
