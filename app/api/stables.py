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

@stable_router.get("/{stable_id}/buildings")
def get_stable_buildings(stable_id: int, db: Session = Depends(get_db), current = Depends(get_current_user)):
    stable = db.query(Stable).filter(Stable.id == stable_id, Stable.owner_id == current.id).first()
    if not stable:
        raise HTTPException(status_code=404, detail="Stable not found")
    return [{"type": "administration"}]  # Для теста этого хватит, доработаешь под свою модель

@stable_router.get("/{stable_id}/boxes")
def get_stable_boxes(stable_id: int, db: Session = Depends(get_db), current = Depends(get_current_user)):
    boxes = db.query(Box).filter(Box.stable_id == stable_id).all()
    return [{"id": b.id, "name": b.name} for b in boxes]
