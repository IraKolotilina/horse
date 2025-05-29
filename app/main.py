from fastapi import FastAPI

from app.api.players import player_router
# из других модулей, если есть ещё роутеры
# from app.api.currency  import currency_router
# from app.api.stables   import stable_router

app = FastAPI()

app.include_router(player_router, prefix="/players", tags=["players"])
# app.include_router(currency_router, prefix="/currency", tags=["currency"])
# app.include_router(stable_router,   prefix="/stables",  tags=["stables"])
