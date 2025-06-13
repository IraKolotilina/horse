from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.players import player_router
from app.api.auth import auth_router
from app.api.horses import horse_router
from app.api.stables import stable_router
from app.api.currency import currency_router

app = FastAPI(title="Horse Management Game")

# CORS settings (при необходимости)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для продакшна лучше ограничить
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(player_router, prefix="/players", tags=["Players"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(horse_router, prefix="/horses", tags=["Horses"])
app.include_router(stable_router, prefix="/stables", tags=["Stables"])
app.include_router(currency_router, prefix="/currency", tags=["Currency"])
