from fastapi import FastAPI
from app.api.auth import auth_router
from app.api.players import player_router
from app.api.currency import router as currency_router
from app.api.stables import stable_router   # если он уже есть

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(player_router, prefix="/players", tags=["players"])
app.include_router(currency_router)    # пути внутри определены
app.include_router(stable_router)      # аналогично
