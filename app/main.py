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

uvicorn.run("main:app")