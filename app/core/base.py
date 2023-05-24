"""Импорты класса Base и всех моделей для Alembic.
Alembic требуется для успешных миграций Base.metadata, а также все модели.
При импорте класса Base в env.py
интерпретатор заодно увидит все остальные модели.
Все новые модели нужно будет импортировать в файл app/core/base.py"""

from app.core.db import Base  # noqa
from app.models.meeting_room import MeetingRoom  # noqa
from app.models.reservation import Reservation  # noqa
