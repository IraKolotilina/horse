from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.player import Player
from app.models.stable import Stable
from app.models.building import Building
from app.models.box     import Box
from app.schemas.stable import StableCreate, StableResponse

stable_router = APIRouter(prefix="/stables", tags=["stables"])

@stable_router.post("", response_model=StableResponse)
def create_stable(
    data: StableCreate,
    db: Session = Depends(get_db),
    current: Player = Depends(get_current_user)
):
    s = Stable(name=data.name, level=1, owner=current)
    db.add(s)
    db.commit()
    db.refresh(s)
    # create admin building
    admin = Building(type="administration", level=1, stable=s)
    db.add(admin)
    # create 2 boxes at lvl1
    for _ in range(2):
        db.add(Box(stable=s))
    db.commit()
    db.refresh(s)
    return s
