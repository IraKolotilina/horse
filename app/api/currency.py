from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.currency import CurrencyUpdate, CurrencyPatch, CurrencyResponse
from app.models.player import Player

router = APIRouter(prefix="/players/me/currency", tags=["currency"])

@router.get("", response_model=CurrencyResponse)
def get_currency(current_user: Player = Depends(get_current_user)):
    return current_user

@router.put("", response_model=CurrencyResponse)
def set_currency(
    update: CurrencyUpdate,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user),
):
    current_user.real_currency = update.real_currency
    current_user.game_currency = update.game_currency
    db.commit()
    db.refresh(current_user)
    return current_user

@router.patch("", response_model=CurrencyResponse)
def patch_currency(
    patch: CurrencyPatch,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user),
):
    new_real = current_user.real_currency + patch.real_currency
    new_game = current_user.game_currency + patch.game_currency
    if new_real < 0 or new_game < 0:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    current_user.real_currency = new_real
    current_user.game_currency = new_game
    db.commit()
    db.refresh(current_user)
    return current_user
