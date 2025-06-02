from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
import random
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.horse import Horse
from app.models.player import Player as PlayerModel
from app.models.stable import Stable
from app.schemas.horse import HorseCreate, HorseResponse

horse_router = APIRouter()

GENES = {
    "speed": ["A", "B", "C"],
    "stamina": ["X", "Y", "Z"],
    "strength": ["P", "Q", "R"]
}

def random_gene(gene_pool):
    return random.choice(gene_pool)

@horse_router.post("/", response_model=HorseResponse)
def create_horse(
    data: HorseCreate,
    db: Session = Depends(get_db),
    current_user: PlayerModel = Depends(get_current_user)
):
    # Проверка: у пользователя есть хотя бы одна конюшня
    stable = db.query(Stable).filter(Stable.owner_id == current_user.id).first()
    if not stable:
        raise HTTPException(status_code=400, detail="No stable available for this user")

    new_horse = Horse(
        id=str(uuid4()),
        name=data.name,
        gender=data.gender,
        breed=data.breed,
        speed=data.speed,
        stamina=data.stamina,
        strength=data.strength,
        gene_speed=random_gene(GENES["speed"]),
        gene_stamina=random_gene(GENES["stamina"]),
        gene_strength=random_gene(GENES["strength"]),
        owner_id=current_user.id,
        stable_id=stable.id,
        is_pregnant=False,
        created_at=datetime.utcnow()
    )

    db.add(new_horse)
    db.commit()
    db.refresh(new_horse)
    return new_horse
