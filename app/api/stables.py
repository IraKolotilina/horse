# app/api/stables.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.stable import StableCreate, StableResponse
from app.models.stable import Stable
from app.models.box import Box
from app.models.building import Building

stable_router = APIRouter(
    prefix="/stables",
    tags=["stables"],
)

@stable_router.post("/", response_model=StableResponse)
def create_stable(
    data: StableCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    stable = Stable(owner_id=current_user.id, name=data.name)
    db.add(stable)
    db.commit()
    db.refresh(stable)

    # Авто-администрация + 2 денника
    admin = Building(stable_id=stable.id, type="administration", level=1)
    db.add(admin)
    for i in (1, 2):
        db.add(Box(stable_id=stable.id, name=f"Box {i}"))
    db.commit()
    db.refresh(stable)
    return stable

@stable_router.get("/", response_model=list[StableResponse])
def list_stables(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return db.query(Stable).filter(Stable.owner_id == current_user.id).all()
