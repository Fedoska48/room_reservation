# объект приложения app
from fastapi import FastAPI

from app.api.meeting_room import router
from app.core.config import settings

# объект приложения с настройками
app = FastAPI(title=settings.app_title, description=settings.app_description)

# подключаем роутер из meeting_room
app.include_router(router)
