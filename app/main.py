from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.auth import auth_router
from app.api.players import player_router
from app.api.currency import currency_router
from app.api.stables import stable_router

# создаём все таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Horse Game API")

app.include_router(auth_router)
app.include_router(player_router)
app.include_router(currency_router)
app.include_router(stable_router)
