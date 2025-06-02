# app/api/currency.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.currency import CurrencyUpdate, CurrencyOut
from app.core.database       import get_db
from app.core.security       import get_current_user
from app.models.player       import Player as PlayerModel

currency_router = APIRouter()

@currency_router.get("/", response_model=CurrencyOut)
def get_balance(current: PlayerModel = Depends(get_current_user)):
    return {
    "real": current.real_currency,
    "game": current.game_currency
}



@currency_router.post("/add", response_model=CurrencyOut)
def add_currency(
    data: CurrencyUpdate,
    db: Session = Depends(get_db),
    current: PlayerModel = Depends(get_current_user)
):
    current.real_currency += data.real
    current.game_currency += data.game
    db.commit()
    db.refresh(current)
    return {
    "real": current.real_currency,
    "game": current.game_currency
}


@currency_router.post("/spend", response_model=CurrencyOut)
def spend_currency(
    data: CurrencyUpdate,
    db: Session = Depends(get_db),
    current: PlayerModel = Depends(get_current_user)
):
    if current.real_currency < data.real or current.game_currency < data.game:
        raise HTTPException(status_code=400, detail="Not enough currency")
    current.real_currency -= data.real
    current.game_currency -= data.game
    db.commit()
    db.refresh(current)
    return {
    "real": current.real_currency,
    "game": current.game_currency
}

