# объект приложения app
from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings

# объект приложения с настройками
app = FastAPI(title=settings.app_title, description=settings.app_description)

# подключаем главный роутер из routers
app.include_router(main_router)
