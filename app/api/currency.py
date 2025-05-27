from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.player import Player
from app.schemas.currency import CurrencyBase, CurrencyUpdate, CurrencyResponse

router = APIRouter(prefix="/players/me/currency", tags=["currency"])

@router.get("", response_model=CurrencyResponse)
def get_currency(current: Player = Depends(get_current_user)):
    return CurrencyResponse(
        real_currency=current.real_currency,
        game_currency=current.game_currency
    )

@router.put("", response_model=CurrencyResponse)
def set_currency(
    payload: CurrencyBase,
    db: Session = Depends(get_db),
    current: Player = Depends(get_current_user),
):
    if payload.real_currency < 0 or payload.game_currency < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Balances cannot be negative")
    current.real_currency = payload.real_currency
    current.game_currency = payload.game_currency
    db.commit()
    db.refresh(current)
    return CurrencyResponse.from_orm(current)

@router.patch("", response_model=CurrencyResponse)
def update_currency(
    payload: CurrencyUpdate,
    db: Session = Depends(get_db),
    current: Player = Depends(get_current_user),
):
    new_real = current.real_currency + payload.real_currency
    new_game = current.game_currency + payload.game_currency
    if new_real < 0 or new_game < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")
    current.real_currency = new_real
    current.game_currency = new_game
    db.commit()
    db.refresh(current)
    return CurrencyResponse.from_orm(current)
