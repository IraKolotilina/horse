from fastapi import FastAPI
from app.models.base import Base
from app.models.base import Base
from app.core.database import engine
from app.api.auth import auth_router
from app.api.players import player_router
from app.api.currency import router as currency_router
from app.api.stables import stable_router

# создаём все таблицы (players, stables, currency-поля и т.д.)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(player_router, prefix="/players", tags=["players"])
app.include_router(currency_router)      # /players/me/currency
app.include_router(stable_router)        # ваши эндпоинты по конюшням и зданиям
