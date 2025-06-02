from fastapi import FastAPI
from app.api.players import player_router
from app.api.auth import auth_router
from app.api.stables import stable_router
from app.api.horses import horse_router


app = FastAPI()

app.include_router(player_router, prefix="/players", tags=["players"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(stable_router, prefix="/stables", tags=["stables"])
app.include_router(horse_router, prefix="/horses", tags=["horses"])

