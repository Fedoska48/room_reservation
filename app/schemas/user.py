from fastapi_users import schemas


# схема с базовыми полями модели пользователя (кроме пароля):
# id, email, is_active, is_superuser, is_verified.
# В скобках указывается тип данных для id пользователя, в нашем случае это int
class UserRead(schemas.BaseUser[int]):
    pass


# обязательные email и password - остальные игнорируются
class UserCreate(schemas.BaseUserCreate):
    pass


# все поля опциональны
# is_active, is_superuser, is_verified - может передать только суперюзер
class UserUpdate(schemas.BaseUserUpdate):
    pass
