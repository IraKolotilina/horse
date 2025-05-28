from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.currency import Currency, CurrencyUpdate, CurrencyDelta
from app.models.player import Player

currency_router = APIRouter(prefix="/players/me/currency", tags=["currency"])

@currency_router.get("/", response_model=Currency)
def get_currency(current_user: Player = Depends(get_current_user)):
    return Currency(
        real_currency=current_user.real_currency,
        game_currency=current_user.game_currency
    )

@currency_router.put("/", response_model=Currency)
def set_currency(
    data: CurrencyUpdate,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user),
):
    current_user.real_currency = data.real_currency
    current_user.game_currency = data.game_currency
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return data

@currency_router.patch("/", response_model=Currency)
def change_currency(
    data: CurrencyDelta,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user),
):
    new_real = current_user.real_currency + data.real_delta
    new_game = current_user.game_currency + data.game_delta
    if new_real < 0 or new_game < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds"
        )
    current_user.real_currency = new_real
    current_user.game_currency = new_game
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return Currency(real_currency=new_real, game_currency=new_game)
