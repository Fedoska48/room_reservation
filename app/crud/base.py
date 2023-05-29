from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    """Для соблюдения стиля DRY, создаем базовый класс для CRUD-операций."""

    def __init__(self, model):
        """При инициализации класса присваивается модель
        и далее все операции производятся над моделью."""
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        """Абстрактный метод для получения объекта по ID."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        db_obj = db_obj.scalars().first()
        return db_obj

    async def get_multi(
            self,
            session: AsyncSession
    ):
        """Абстрактный метод для получения списка объектов."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        """Абстрактный метод для создания объекта."""
        # конвертация в словарь
        new_obj_data = obj_in.dict()

        # если пользователь передан
        if user is not None:
            # дополняем словарь с данными для создания
            new_obj_data['user_id'] = user.id
        # создаем объект модели
        # В параметры передаём пары "ключ=значение",
        # для этого распаковываем словарь
        db_obj = self.model(**new_obj_data)

        # сессия уже создана асинх.генератором и передается вторым параметром
        # добавляем объект в сессию
        session.add(db_obj)
        # записываем данные в БД
        await session.commit()
        # Обновляем объект, чтобы вернуть его данные
        await session.refresh(db_obj)
        # Возвращаем только что созданный объект
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession
    ):
        """Абстрактное обновление объекта."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ):
        """Абстрактное удаление объекта."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj
