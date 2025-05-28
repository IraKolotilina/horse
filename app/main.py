# app/main.py
from fastapi import FastAPI

from app.api.auth      import auth_router
from app.api.players   import player_router
from app.api.currency  import currency_router
from app.api.stables   import stable_router

from app.core.database import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth_router,    prefix="/auth")
app.include_router(player_router,  prefix="/players")
app.include_router(currency_router)
app.include_router(stable_router)
