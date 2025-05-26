from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import player, currency
from app.api.auth import auth_router
from app.api.players import player_router

Base.metadata.create_all(bind=engine)
print("✅ Таблицы успешно созданы в базе данных")

app = FastAPI(title="Horse Game API", version="1.0")

app.include_router(auth_router)
app.include_router(player_router)

@app.get("/status")
def status():
    return { "status": "OK" }