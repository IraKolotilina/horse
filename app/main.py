from fastapi import FastAPI

from app.api.auth     import auth_router
from app.api.players  import player_router
from app.api.currency import router as currency_router
from app.api.stables  import stable_router   # ← if you’ve implemented stables

app = FastAPI()

app.include_router(auth_router)
app.include_router(player_router)
app.include_router(currency_router)
app.include_router(stable_router)      # ← likewise
