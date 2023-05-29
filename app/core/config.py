from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Необходимо указать требуемые переменные из '.env'. Или дефолтные знач.
    Регистронезависим.Имя атрибута класса должно совпадать именем переменной"""
    app_title: str = 'Бронирование переговорок'
    app_description: str = 'Эффективное использование переговорок'
    database_url: str
    secret: str
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None


    class Config:
        # полный путь прописывать не обязательно,
        # но это способ работеает через запуск uvicorn
        # иначе полный или относительный путь, либо в параметры uvicorn.run()
        env_file = '.env'


# создадим глобальную переменную, для вызова атрибутов через settings.app_title
# если обращаться к классу Settings().app_title, то каждый раз будет обращение
# к файлу .env на жестком диске, а это медленная операция
settings = Settings()
