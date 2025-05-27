# app/api/currency.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.currency import CurrencyResponse, CurrencyUpdate, CurrencyChange
from app.models.player import Player

currency_router = APIRouter(
    prefix="/players/me/currency",
    tags=["currency"],
)

@currency_router.get("/", response_model=CurrencyResponse)
def get_currency(current_user: Player = Depends(get_current_user)):
    return CurrencyResponse(real=current_user.real_currency, game=current_user.game_currency)

@currency_router.put("/", response_model=CurrencyResponse)
def set_currency(
    data: CurrencyUpdate,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user),
):
    current_user.real_currency = data.real
    current_user.game_currency = data.game
    db.commit()
    return CurrencyResponse(real=current_user.real_currency, game=current_user.game_currency)

@currency_router.patch("/", response_model=CurrencyResponse)
def change_currency(
    delta: CurrencyChange,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user),
):
    new_real = current_user.real_currency + delta.real
    new_game = current_user.game_currency + delta.game
    if new_real < 0 or new_game < 0:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    current_user.real_currency = new_real
    current_user.game_currency = new_game
    db.commit()
    return CurrencyResponse(real=new_real, game=new_game)
