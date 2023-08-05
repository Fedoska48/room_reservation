from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle):
    """Создать гугл-таблицу."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheets_body = {
        'properties': {
            'title': f'Report {now_date_time}',
            'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'List1',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 11
                }
            }
        }]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheets_body)
    )
    spreadsheetsId = response['spreadsheetId']
    return spreadsheetsId


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """Выдать разрешение пользователю."""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        reservations: list,
        wrapper_services: Aiogoogle
) -> None:
    """Записать данные из БД в гугл-таблицу."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    # Здесь формируется тело таблицы
    table_values = [
        ['Отчет от', now_date_time],
        ['Количество регистраций переговорок'],
        ['ID переговорки', 'Кол-во бронирований']
    ]
    # Здесь в таблицу добавляются строчки
    for res in reservations:
        new_row = [str(res['meetingroom_id']), str(res['count'])]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
