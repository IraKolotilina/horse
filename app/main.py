# app/main.py
from fastapi import FastAPI
from app.api.auth     import auth_router
from app.api.players  import player_router
from app.api.currency import currency_router
from app.api.stables  import stable_router

from app.core.database import Base, engine

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(player_router)
app.include_router(currency_router)
app.include_router(stable_router)
