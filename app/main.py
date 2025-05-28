from fastapi import FastAPI
from app.core.database import init_db
from app.api.auth import auth_router
from app.api.players import player_router
from app.api.currency import currency_router
from app.api.stables import stable_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

# аутентикация
app.include_router(auth_router, prefix="/auth", tags=["auth"])
# CRUD для игроков, профиль, обновление email/password
app.include_router(player_router, prefix="/players", tags=["players"])
# работа с валютой
app.include_router(currency_router, prefix="/players/me/currency", tags=["currency"])
# всё про конюшни (stables, boxes, buildings и т.п.)
app.include_router(stable_router, prefix="/players/{player_id}/stables", tags=["stables"])
