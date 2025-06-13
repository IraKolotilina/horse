from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.stable import StableCreate, StableOut, BoxOut, BuildingCreate, BuildingOut
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.stable import Stable
from app.models.box import Box
from app.models.building import Building
from app.models.player import Player
from app.models.horse import Horse

stable_router = APIRouter()

# Типы зданий и лимиты
BUILDING_TYPES = {
    "field": None,
    "lumber_mill": None,
    "pasture": None,
    "garage": 1,
    "shop": 1,
    "warehouse": 1,
    "vet_box": 1,
    "track": 1,
    "arena": 1,
    "plaza": 1,
    "race_track": 1,
    "administration": 1,
    "stable": 1
}

MAX_RESOURCE_BUILDINGS = 9  # поле + лесопилка + пастбище


@stable_router.post("/", response_model=StableOut)
def create_stable(
    data: StableCreate,
    db: Session = Depends(get_db),
    current: Player = Depends(get_current_user)
):
    # Создание Stable
    new = Stable(name=data.name, owner_id=current.id)
    db.add(new)
    db.flush()

    # Автоматически создаём здание "administration"
    admin_building = Building(
        type="administration",
        level=1,
        stable_id=new.id
    )
    db.add(admin_building)

    # Количество боксов = уровню stable (по умолчанию 1)
    for i in range(new.level):
        db.add(Box(name=f"Box {i+1}", stable_id=new.id))

    db.commit()
    db.refresh(new)
    return new


@stable_router.get("/", response_model=list[StableOut])
def list_stables(
    db: Session = Depends(get_db),
    current: Player = Depends(get_current_user)
):
    return db.query(Stable).filter(Stable.owner_id == current.id).all()


@stable_router.get("/{stable_id}/boxes", response_model=list[BoxOut])
def get_boxes(
    stable_id: str,
    db: Session = Depends(get_db),
    current: Player = Depends(get_current_user)
):
    return db.query(Box).filter(Box.stable_id == stable_id).all()


@stable_router.get("/{stable_id}/buildings", response_model=list[BuildingOut])
def get_stable_buildings(
    stable_id: str,
    db: Session = Depends(get_db),
    current: Player = Depends(get_current_user)
):
    return db.query(Building).filter(Building.stable_id == stable_id).all()


@stable_router.post("/{stable_id}/buildings", response_model=BuildingOut)
def build_building(
    stable_id: str,
    data: BuildingCreate,
    db: Session = Depends(get_db),
    current: Player = Depends(get_current_user)
):
    stable = db.query(Stable).filter(
        Stable.id == stable_id,
        Stable.owner_id == current.id
    ).first()
    if not stable:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Stable not found")

    btype = data.type
    blevel = data.level

    if btype not in BUILDING_TYPES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid building type")

    existing = db.query(Building).filter(
        Building.stable_id == stable_id,
        Building.type == btype
    ).all()

    # Единственность по типу
    limit = BUILDING_TYPES[btype]
    if limit is not None and len(existing) >= limit:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{btype} already exists")

    # Ресурсные здания: суммарно не более 9
    if limit is None:
        total = db.query(Building).filter(
            Building.stable_id == stable_id,
            Building.type.in_(["field", "pasture", "lumber_mill"])
        ).count()
        if total + 1 > MAX_RESOURCE_BUILDINGS:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Resource building limit reached")

    # Повышение уровня stable ("конюшни")
    if btype == "stable":
        if blevel > stable.level:
            # Проверка: нельзя повысить stable выше порога, пока все остальные здания не равны этому порогу
            threshold = (stable.level // 5) * 5 + 5
            if blevel > threshold:
                raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                    f"Cannot raise stable above level {threshold} without all buildings being level {threshold}")
            all_buildings = db.query(Building).filter(
                Building.stable_id == stable_id,
                Building.type != "stable"
            ).all()
            if not all(b.level >= threshold for b in all_buildings):
                raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                    f"All other buildings must be at least level {threshold} to upgrade stable")

            # Если всё ок, обновляем уровень stable
            stable.level = blevel

            # Синхронизация количества боксов
            current_boxes = db.query(Box).filter(Box.stable_id == stable_id).count()
            if blevel > current_boxes:
                for i in range(current_boxes, blevel):
                    db.add(Box(name=f"Box {i+1}", stable_id=stable.id))

            db.commit()
            db.refresh(stable)

    # Ограничение: прочие здания не могут быть выше уровня stable
    elif blevel > stable.level:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            f"{btype} level cannot exceed stable level ({stable.level})")

    building = next((b for b in existing if b.type == btype), None)
    if building:
        building.level = blevel
    else:
        building = Building(
            type=btype,
            level=blevel,
            stable_id=stable_id,
        )
        db.add(building)

    db.commit()
    db.refresh(building)
    return building
