from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.stable import Stable
from app.models.box import Box

stable_router = APIRouter(prefix="/stables", tags=["stables"])

@stable_router.post("/", status_code=status.HTTP_200_OK)
def create_stable(
    data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    name = data.get("name")
    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name is required"
        )
    stable = Stable(name=name, owner_id=current_user.id)
    db.add(stable)
    db.commit()
    db.refresh(stable)

    # после создания для уровня 1 по ТЗ создаём два бокса
    for _ in range(2):
        box = Box(stable_id=stable.id)
        db.add(box)
    db.commit()

    return {"id": stable.id, "name": stable.name, "level": stable.level}

@stable_router.get("/", status_code=status.HTTP_200_OK)
def list_stables(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    stables = db.query(Stable).filter(Stable.owner_id == current_user.id).all()
    return [
        {"id": s.id, "name": s.name, "level": s.level,
         "boxes": [b.id for b in s.boxes]}
        for s in stables
    ]
