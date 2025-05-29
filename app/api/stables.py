# app/api/stables.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.stable  import StableCreate, StableOut
from app.core.database   import get_db
from app.core.security   import get_current_user
from app.models.stable   import Stable
from app.models.box      import Box

stable_router = APIRouter()

@stable_router.post("/", response_model=StableOut)
def create_stable(
    data: StableCreate,
    db: Session = Depends(get_db),
    current = Depends(get_current_user)
):
    new = Stable(name=data.name, owner_id=current.id)
    db.add(new)
    db.commit()
    db.refresh(new)
    # при level == 1 создаём 2 бокса
    if new.level == 1:
        for i in range(1, 3):
            b = Box(name=f"Box {i}", stable_id=new.id)
            db.add(b)
        db.commit()
    db.refresh(new)
    return new

@stable_router.get("/", response_model=list[StableOut])
def list_stables(
    db: Session = Depends(get_db),
    current = Depends(get_current_user)
):
    return db.query(Stable).filter(Stable.owner_id == current.id).all()
