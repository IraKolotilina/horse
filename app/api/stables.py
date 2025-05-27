from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.player import Player
from app.models.stable import Stable
from app.models.box import Box
from app.models.building import Building
from app.schemas.stable import StableCreate, StableResponse

stable_router = APIRouter(prefix="/stables", tags=["stables"])

@stable_router.post("/", response_model=StableResponse)
def create_stable(
    data: StableCreate,
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_user)
):
    # создаём конюшню
    new = Stable(name=data.name, player_id=current_user.id)
    db.add(new)
    db.commit()
    db.refresh(new)

    # админка
    admin = Building(type="administration", level=1, stable_id=new.id)
    db.add(admin)
    # два денника
    for _ in range(2):
        db.add(Box(stable_id=new.id))
    db.commit()

    return new
