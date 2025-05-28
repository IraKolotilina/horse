# app/api/currency.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.player import Player
from app.schemas.currency import Currency

currency_router = APIRouter(
    prefix="/players/me/currency",
    tags=["currency"],
)

@currency_router.get("/", response_model=Currency)
def get_currency(
    current_user: Player = Depends(get_current_user)
):
    return {"real": current_user.real_currency, "game": current_user.game_currency}

@currency_router.put("/", response_model=Currency)
def set_currency(
    currency: Currency,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user)
):
    current_user.real_currency = currency.real
    current_user.game_currency = currency.game
    db.commit()
    db.refresh(current_user)
    return {"real": current_user.real_currency, "game": current_user.game_currency}

@currency_router.patch("/", response_model=Currency)
def update_currency(
    delta: Currency,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user)
):
    new_real = current_user.real_currency + delta.real
    new_game = current_user.game_currency + delta.game
    if new_real < 0 or new_game < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds"
        )
    current_user.real_currency = new_real
    current_user.game_currency = new_game
    db.commit()
    db.refresh(current_user)
    return {"real": new_real, "game": new_game}
