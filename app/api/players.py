from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user  # уже есть
from app.models.player import Player
from app.schemas.player import (
    PlayerCreate, PlayerResponse, PlayerUpdate,
    CurrencyResponse, CurrencySet, CurrencyDelta,
)
from app.core.security import hash_password  # для профиля

player_router = APIRouter(prefix="/players", tags=["players"])

# ... существующие register/get_profile/update_profile ...

@player_router.get("/me/currency", response_model=CurrencyResponse)
def get_currency(current_user: Player = Depends(get_current_user)):
    return {"real": current_user.real_currency,
            "game": current_user.game_currency}

@player_router.put("/me/currency", response_model=CurrencyResponse)
def set_currency(
    payload: CurrencySet,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user),
):
    current_user.real_currency = payload.real
    current_user.game_currency = payload.game
    db.commit()
    db.refresh(current_user)
    return {"real": current_user.real_currency,
            "game": current_user.game_currency}

@player_router.patch("/me/currency", response_model=CurrencyResponse)
def delta_currency(
    delta: CurrencyDelta,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user),
):
    new_real = current_user.real_currency + (delta.real or 0)
    new_game = current_user.game_currency + (delta.game or 0)

    # Проверка на перерасход
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
