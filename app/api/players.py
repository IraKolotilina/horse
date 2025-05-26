from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerResponse, PlayerUpdate
from app.core.security import get_current_user, hash_password

player_router = APIRouter(prefix="/players", tags=["players"])


@player_router.post("/", response_model=PlayerResponse)
def register_player(player: PlayerCreate, db: Session = Depends(get_db)):
    existing_username = db.query(Player).filter(Player.username == player.username).first()
    existing_email = db.query(Player).filter(Player.email == player.email).first()

    if existing_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(player.password)
    new_player = Player(
        username=player.username,
        email=player.email,
        password=hashed_password
    )
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player


@player_router.get("/me", response_model=PlayerResponse)
def get_profile(current_user: Player = Depends(get_current_user)):
    return current_user


@player_router.put("/me", response_model=PlayerResponse)
def update_profile(
    update: PlayerUpdate,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user)
):
    if update.email:
        existing_email = db.query(Player).filter(Player.email == update.email).first()
        if existing_email and existing_email.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = update.email

    if update.password:
        current_user.password = hash_password(update.password)

    db.commit()
    db.refresh(current_user)
    return current_user
