# Здесь будет храниться код, ответственный за подключение к базе данных
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr

from app.core.config import settings


class PreBase:
    """Расширяем базовый класс Base однотипными настройками для всех таблиц."""

    @declared_attr
    def __tablename__(cls):
        """Делаем дефолтные названия для всех таблиц."""
        return cls.__name__.lower()

    # делаем наличие поля ID в таблицах обязательным по-умолчанию
    id = Column(Integer, primary_key=True)


# базовый класс для моделей
Base = declarative_base(cls=PreBase)

# асинхронный движок
engine = create_async_engine(settings.database_url)

# создание асинхронной сессии (один объект сессии)
# async_session = AsyncSession(engine)

# для множественного создания сессий
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
