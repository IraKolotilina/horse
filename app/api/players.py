from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.player  import PlayerCreate, PlayerOut, PlayerUpdate
from app.schemas.currency import CurrencyUpdate, CurrencyOut
from app.core.database   import get_db
from app.core.security   import hash_password, get_current_user
from app.models.player   import Player as PlayerModel

player_router = APIRouter()

@player_router.post("/", response_model=PlayerOut)
def register_player(user: PlayerCreate, db: Session = Depends(get_db)):
    # тесты ожидают ошибку только для username, но реализуем оба варианта
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

@player_router.get("/me", response_model=PlayerOut)
def read_profile(current: PlayerModel = Depends(get_current_user)):
    return current

@player_router.put("/me", response_model=PlayerOut)
def update_profile(
    data: PlayerUpdate,
    db: Session = Depends(get_db),
    current: PlayerModel = Depends(get_current_user),
):
    # тест ждет 200 даже с пустым payload, просто возвращаем пользователя как есть
    if not data.email and not data.password:
        return current
    if data.email:
        current.email = data.email
    if data.password:
        current.password = hash_password(data.password)
    db.commit()
    db.refresh(current)
    return current

# --- Currency endpoints as subroutes ---

@player_router.get("/me/currency", response_model=CurrencyOut)
def get_balance(current: PlayerModel = Depends(get_current_user)):
    return {
        "real": current.real_currency,
        "game": current.game_currency
    }

@player_router.put("/me/currency", response_model=CurrencyOut)
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

@player_router.patch("/me/currency", response_model=CurrencyOut)
def spend_currency(
    data: CurrencyUpdate,
    db: Session = Depends(get_db),
    current: PlayerModel = Depends(get_current_user)
):
    # Тебе нужно брать по модулю для списания:
    real_spend = abs(data.real)
    game_spend = abs(data.game)
    if current.real_currency < real_spend or current.game_currency < game_spend:
        raise HTTPException(status_code=400, detail="Not enough currency")
    current.real_currency -= real_spend
    current.game_currency -= game_spend
    db.commit()
    db.refresh(current)
    return {
        "real": current.real_currency,
        "game": current.game_currency
    }
from pydantic import BaseModel, EmailStr

class PlayerUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

@player_router.put("/update")
def update_player_profile(
    data: PlayerUpdate,
    db: Session = Depends(get_db),
    current_user: PlayerModel = Depends(get_current_user)
):
    user = db.query(PlayerModel).filter(PlayerModel.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.email:
        user.email = data.email

    if data.password:
        from app.core.security import get_password_hash
        user.password = get_password_hash(data.password)

    db.commit()
    return {"detail": "Profile updated"}
