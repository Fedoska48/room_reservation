# app/models/__init__.py
# «сообщим» интерпрертатору о модели Reservation до того, как он приступит
# к выполнению кода т.к. в файле models/meeting_room.py указана ссылка
# на строку 'Reservation', а не на модель Reservation (можно и так, и так)
# однако, указание самой модели сработает не всегда из-за циклических импортов
# при потенциальном доступе в обоих моделях друг к другу
# MeetingRoom тут за компанию
from .meeting_room import MeetingRoom
from .reservation import Reservation
from .user import User
