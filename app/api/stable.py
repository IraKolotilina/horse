from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.stable import Stable
from app.models.box import Box
from app.models.building import Building
from app.schemas.stable import StableCreate, StableResponse

stable_router = APIRouter(
    prefix="/stables",
    tags=["stables"],
    dependencies=[Depends(get_current_user)]
)

@stable_router.post("/", response_model=StableResponse)
def create_stable(
    data: StableCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # создаём саму конюшню
    new = Stable(name=data.name, level=1, player_id=current_user.id)
    db.add(new)
    db.commit()
    db.refresh(new)

    # 2 денника
    for _ in range(2):
        db.add(Box(stable_id=new.id))

    # административное здание
    db.add(Building(stable_id=new.id, type="administration", level=1))

    db.commit()
    db.refresh(new)
    return new

@stable_router.get("/", response_model=list[StableResponse])
def list_stables(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Stable).filter(Stable.player_id == current_user.id).all()
