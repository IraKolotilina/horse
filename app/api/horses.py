from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
import random
from typing import Optional
from datetime import datetime, timezone
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.horse import Horse
from app.models.player import Player as PlayerModel
from app.models.stable import Stable
from app.schemas.horse import HorseCreate, HorseResponse, HorseBreedRequest, HorseUpdate


horse_router = APIRouter()

GENES = {
    "speed": ["A", "B", "C"],
    "stamina": ["X", "Y", "Z"],
    "strength": ["P", "Q", "R"],
    "jump": ["J", "K", "L"]
}

def inherit_stat(mother_val, father_val):
    return round((mother_val + father_val) / 2 + random.uniform(-1, 1), 1)

def random_gene_pair(g1, g2):
    return random.choice([g1, g2])

def random_gene(gene_pool):
    return random.choice(gene_pool)

@horse_router.post("/", response_model=HorseResponse)
def create_horse(
    data: HorseCreate,
    db: Session = Depends(get_db),
    current_user: PlayerModel = Depends(get_current_user)
):
    stable = db.query(Stable).filter(
        Stable.owner_id == current_user.id
    ).first()

    if not stable:
        raise HTTPException(status_code=400, detail="No available stable found for this user.")

    new_horse = Horse(
        id=str(uuid4()),
        name=data.name,
        gender=data.gender,
        breed=data.breed,
        speed=data.speed,
        stamina=data.stamina,
        strength=data.strength,
        jump=data.jump,
        height=data.height,
        type=data.type or "standard",
        age=0,
        gene_speed=random_gene(GENES["speed"]),
        gene_stamina=random_gene(GENES["stamina"]),
        gene_strength=random_gene(GENES["strength"]),
        gene_jump=random_gene(GENES["jump"]),
        owner_id=current_user.id,
        stable_id=stable.id,
        is_pregnant=False,
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_horse)
    db.commit()
    db.refresh(new_horse)
    return new_horse

@horse_router.post("/breed", response_model=HorseResponse)
def breed_horse(
    request: HorseBreedRequest,
    db: Session = Depends(get_db),
    current_user: PlayerModel = Depends(get_current_user)
):
    mother = db.query(Horse).filter(Horse.id == request.mother_id, Horse.owner_id == current_user.id).first()
    father = db.query(Horse).filter(Horse.id == request.father_id, Horse.owner_id == current_user.id).first()

    if not mother or not father:
        raise HTTPException(status_code=404, detail="Both parents must exist and belong to the player.")

    if mother.age < 4 or father.age < 4:
        raise HTTPException(status_code=400, detail="Оба родителя должны быть старше 4 лет.")

    stable = db.query(Stable).filter(Stable.id == mother.stable_id, Stable.owner_id == current_user.id).first()
    if not stable:
        raise HTTPException(status_code=400, detail="No stable found for breeding.")

    foal = Horse(
        id=str(uuid4()),
        name=request.foal_name,
        gender=random.choice(["male", "female"]),
        breed=mother.breed if mother.breed == father.breed else "mixed",
        speed=inherit_stat(mother.speed, father.speed),
        stamina=inherit_stat(mother.stamina, father.stamina),
        strength=inherit_stat(mother.strength, father.strength),
        jump=inherit_stat(mother.jump, father.jump),
        height=inherit_stat(mother.height, father.height),
        age=0,
        type="legendary" if mother.type == "legendary" and father.type == "legendary" else "standard",
        gene_speed=random_gene_pair(mother.gene_speed, father.gene_speed),
        gene_stamina=random_gene_pair(mother.gene_stamina, father.gene_stamina),
        gene_strength=random_gene_pair(mother.gene_strength, father.gene_strength),
        gene_jump=random_gene_pair(mother.gene_jump, father.gene_jump),
        owner_id=current_user.id,
        stable_id=mother.stable_id,
        is_pregnant=False,
        created_at=datetime.now(timezone.utc)
    )

    db.add(foal)
    db.commit()
    db.refresh(foal)
    return foal

@horse_router.patch("/{horse_id}", response_model=HorseResponse)
def update_horse(
    horse_id: str,
    updates: HorseUpdate,
    db: Session = Depends(get_db),
    current_user: PlayerModel = Depends(get_current_user)
):
    horse = db.query(Horse).filter(Horse.id == horse_id, Horse.owner_id == current_user.id).first()
    if not horse:
        raise HTTPException(status_code=404, detail="Horse not found")

    for field, value in updates.dict(exclude_unset=True).items():
        setattr(horse, field, value)

    db.commit()
    db.refresh(horse)
    return horse
