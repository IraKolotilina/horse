from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.player import PlayerCreate, PlayerOut, PlayerUpdate
from app.schemas.currency import CurrencyUpdate, CurrencyOut
from app.core.database import get_db
from app.core.security import hash_password, get_current_user
from app.models.player import Player as PlayerModel

player_router = APIRouter()


# -------------------- Регистрация --------------------
@player_router.post("/", response_model=PlayerOut)
def register_player(user: PlayerCreate, db: Session = Depends(get_db)):
    if db.query(PlayerModel).filter(PlayerModel.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    if db.query(PlayerModel).filter(PlayerModel.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    db_user = PlayerModel(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# -------------------- Получение профиля --------------------
@player_router.get("/me", response_model=PlayerOut)
def read_profile(current: PlayerModel = Depends(get_current_user)):
    return current


# -------------------- Обновление профиля --------------------
@player_router.put("/me", response_model=PlayerOut)
def update_profile(
    data: PlayerUpdate,
    db: Session = Depends(get_db),
    current: PlayerModel = Depends(get_current_user),
):
    if data.email:
        current.email = data.email
    if data.password:
        current.password = hash_password(data.password)
    db.commit()
    db.refresh(current)
    return current


# -------------------- Получение валюты --------------------
@player_router.get("/me/currency", response_model=CurrencyOut)
def get_balance(current: PlayerModel = Depends(get_current_user)):
    return {
        "real": current.real_currency,
        "game": current.game_currency
    }


# -------------------- Установка валюты (PUT) --------------------
@player_router.put("/me/currency", response_model=CurrencyOut)
def set_currency(
    data: CurrencyUpdate,
    db: Session = Depends(get_db),
    current: PlayerModel = Depends(get_current_user)
):
    current.real_currency = data.real or 0
    current.game_currency = data.game or 0
    db.commit()
    db.refresh(current)
    return {
        "real": current.real_currency,
        "game": current.game_currency
    }


# -------------------- Изменение валюты (PATCH) --------------------
@player_router.patch("/me/currency", response_model=CurrencyOut)
def change_currency(
    data: CurrencyUpdate,
    db: Session = Depends(get_db),
    current: PlayerModel = Depends(get_current_user)
):
    new_real = current.real_currency + (data.real or 0)
    new_game = current.game_currency + (data.game or 0)

    if new_real < 0 or new_game < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds"
        )

    current.real_currency = new_real
    current.game_currency = new_game
    db.commit()
    db.refresh(current)
    return {
        "real": current.real_currency,
        "game": current.game_currency
    }
