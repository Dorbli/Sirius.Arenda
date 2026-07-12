from fastapi import FastAPI
from routers.rooms_router import router as r_router
from database.database import init_db 
from routers.booking_router import router as b_router
from routers.auth_router import router as a_router
import uvicorn

# Создаём приложение
app = FastAPI(
    title="Сириус.Аренда",
    description="API для сервиса бронирования пространств",
    version="1.0.0"
)

init_db()

app.include_router(r_router, tags=['rooms'])
app.include_router(b_router, tags=['bookings'])
app.include_router(a_router, tags=['auth'])

# Корневой эндпоинт для проверки
# @app.get("/")
# def root():
#     return {
#         "message": "Добро пожаловать в систему управления.",
#         "endpoints": {
#             "GET /rooms": "Список всех комнат",
#             "POST /rooms": "Создать комнату",
#             "GET /rooms/{id}": "Информация о комнате",
#             "PUT /rooms/{id}": "Обновить комнату",
#             "DELETE /rooms/{id}": "Удалить комнату",
#             "POST /bookings": "Создание бронирования",
#             "DELETE /bookings/{id}": "Отмена бронирования",
#             "GET /rooms/{id}/bookings?date=YYYY-MM-DD": "Получение списка бронирований для конкретной комнаты на выбранную дату"
#         }
#     }

uvicorn.run(
    "main:app",  # Запускаем main.py → app
    host="0.0.0.0",
    port=8000,
    reload=False  # Автоматический перезапуск при изменениях
)