from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.stable import Stable, Box, Building
from app.schemas.stable import StableCreate, StableResponse

router = APIRouter(prefix="/stables", tags=["stables"])

@router.post("", response_model=StableResponse)
def create_stable(
    data: StableCreate,
    db: Session = Depends(get_db),
    owner=Depends(get_current_user),
):
    # создаём конюшню
    stable = Stable(name=data.name, level=1, owner_id=owner.id)
    db.add(stable)
    db.flush()  # присвоит stable.id
    # автоматом строим админ. здание
    admin = Building(
        stable_id=stable.id, type="administration", level=1
    )
    db.add(admin)
    # создаём 2 денника
    for _ in range(2):
        db.add(Box(stable_id=stable.id, occupied=False))
    db.commit()
    db.refresh(stable)
    return stable
