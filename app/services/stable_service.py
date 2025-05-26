from sqlalchemy.orm import Session
from app.models.stable import Stable
from app.models.building import Building
from app.models.player import Player
from app.schemas.stable import StableCreate
from fastapi import HTTPException, status

def create_stable(db: Session, player: Player, stable_data: StableCreate) -> Stable:
    # Создание новой конюшни
    new_stable = Stable(name=stable_data.name, owner_id=player.id)
    db.add(new_stable)
    db.flush()  # Получить ID для ForeignKey

    # Добавление здания администрации уровня 1
    admin_building = Building(type="administration", level=1, stable_id=new_stable.id)
    db.add(admin_building)

    db.commit()
    db.refresh(new_stable)
    return new_stable
