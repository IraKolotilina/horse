from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.player import Player
from app.schemas.currency import CurrencyResponse, CurrencyUpdate, CurrencyPatch

router = APIRouter(
    prefix="/players/me/currency",
    tags=["currency"],
)

@router.get("/", response_model=CurrencyResponse)
def get_currency(current_user: Player = Depends(get_current_user)):
    return {"real": current_user.real_currency, "game": current_user.game_currency}

@router.put("/", response_model=CurrencyResponse)
def set_currency(
    update: CurrencyUpdate,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user),
):
    current_user.real_currency = update.real
    current_user.game_currency = update.game
    db.commit()
    db.refresh(current_user)
    return {"real": update.real, "game": update.game}

@router.patch("/", response_model=CurrencyResponse)
def change_currency(
    patch: CurrencyPatch,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user),
):
    new_real = current_user.real_currency + patch.real
    new_game = current_user.game_currency + patch.game
    if new_real < 0 or new_game < 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Insufficient funds")
    current_user.real_currency = new_real
    current_user.game_currency = new_game
    db.commit()
    db.refresh(current_user)
    return {"real": new_real, "game": new_game}
