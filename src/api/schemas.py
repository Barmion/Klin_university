# api/schemas.py
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiResponse

IMPORT_EXCEL_SCHEMA = {
    'description': """
## Массовый импорт сотрудников из Excel файла

### Пример данных в Excel:
| first_name | last_name | middle_name | email | position | is_active |
|------------|-----------|-------------|-------|----------|-----------|
| Иван | Петров | Сергеевич | ivan@example.com | Разработчик | TRUE |
| Мария | Сидорова | Ивановна | maria@example.com | Дизайнер | FALSE |
    """,
    'request': {
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'file': {
                    'type': 'string',
                    'format': 'binary',
                    'description': 'Excel файл с данными сотрудников'
                }
            },
            'required': ['file']
        }
    },
    'responses': {
        201: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    'Успешный импорт с созданными записями',
                    value={
                        'Записей добавлено': 3,
                        'Добавленые записи': [
                            {
                                'id': 1,
                                'first_name': 'Иван',
                                'last_name': 'Петров',
                                'middle_name': 'Сергеевич',
                                'email': 'ivan@example.com',
                                'position': 'Разработчик',
                                'is_active': True
                            }
                        ],
                        'Ошибок валидации': 1,
                        'Записи с ошибками': [
                            {
                                'data': {
                                    'first_name': 'Ошибка',
                                    'last_name': 'Тест',
                                    'email': 'invalid-email'
                                },
                                'errors': {
                                    'email': ['Введите правильный адрес электронной почты.']
                                }
                            }
                        ]
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    'Неверный формат файла',
                    value={
                        'error': 'Неверный формат файла',
                        'message': 'Поддерживаются только Excel файлы (.xlsx, .xls)'
                    }
                ),
                OpenApiExample(
                    'Файл не загружен',
                    value={
                        'error': 'Файл не найден', 
                        'message': 'Пожалуйста, прикрепите Excel файл'
                    }
                ),
                OpenApiExample(
                    'Ошибка парсинга Excel',
                    value={
                        'error': 'Ошибка чтения файла',
                        'message': 'Файл поврежден или имеет неверный формат'
                    }
                ),
                OpenApiExample(
                    'Импорт с ошибками валидации',
                    value={
                        'Записей добавлено': 0,
                        'Добавленые записи': [],
                        'Ошибок валидации': 2,
                        'Записи с ошибками': [
                            {
                                'data': {'first_name': '', 'last_name': 'Тест', 'email': 'test@example.com'},
                                'errors': {'first_name': ['Это поле не может быть пустым.']}
                            },
                            {
                                'data': {'first_name': 'Иван', 'last_name': 'Петров', 'email': 'invalid'},
                                'errors': {'email': ['Введите правильный адрес электронной почты.']}
                            }
                        ]
                    }
                ),
            ]
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    'Требуется авторизация',
                    value={
                        'detail': 'Учетные данные не были предоставлены.'
                    }
                )
            ]
        )
    },
    'tags': ['api'],
    'methods': ['POST']
}
