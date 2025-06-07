# app/api/stables.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.stable import StableCreate, StableOut, BoxOut
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.stable import Stable
from app.models.box import Box
from app.models.player import Player
from app.models.horse import Horse

stable_router = APIRouter()

@stable_router.post("/", response_model=StableOut)
def create_stable(
    data: StableCreate,
    db: Session = Depends(get_db),
    current: Player = Depends(get_current_user)
):
    new = Stable(name=data.name, owner_id=current.id)
    db.add(new)
    db.flush()  # получаем new.id до коммита

    # при level == 1 создаём 2 бокса
    if new.level == 1:
        for i in range(1, 3):
            b = Box(name=f"Box {i}", stable_id=new.id)
            db.add(b)

    db.commit()
    db.refresh(new)  # подгружаем все relationships
    return new

@stable_router.get("/", response_model=list[StableOut])
def list_stables(
    db: Session = Depends(get_db),
    current: Player = Depends(get_current_user)
):
    return db.query(Stable).filter(Stable.owner_id == current.id).all()

@stable_router.get("/{stable_id}/buildings")
def get_stable_buildings(
    stable_id: str,
    db: Session = Depends(get_db),
    current: Player = Depends(get_current_user)
):
    stable = db.query(Stable).filter(
        Stable.id == stable_id,
        Stable.owner_id == current.id
    ).first()
    if not stable:
        raise HTTPException(status_code=404, detail="Stable not found")

    # Здесь можно возвращать настоящие здания, пока мок
    return [{"type": "administration"}]

@stable_router.get("/{stable_id}/boxes", response_model=list[BoxOut])
def get_stable_boxes(
    stable_id: str,
    db: Session = Depends(get_db),
    current: Player = Depends(get_current_user)
):
    stable = db.query(Stable).filter(
        Stable.id == stable_id,
        Stable.owner_id == current.id
    ).first()
    if not stable:
        raise HTTPException(status_code=404, detail="Stable not found")

    return db.query(Box).filter(Box.stable_id == stable.id).all()
