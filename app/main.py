from fastapi import FastAPI

from app.core.database import init_db
from app.api.players   import player_router
from app.api.auth      import auth_router
from app.api.currency  import currency_router
from app.api.stables   import stable_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(player_router)
app.include_router(auth_router)
app.include_router(currency_router)
app.include_router(stable_router)
