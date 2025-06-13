from sqlalchemy.orm import Session
from app.models.stable import Stable
from app.models.building import Building
from app.models.box import Box
from app.schemas.stable import StableCreate

def create_stable(db: Session, player_id: int, stable_data: StableCreate):
    # Создаем stable
    db_stable = Stable(name=stable_data.name, level=1, owner_id=player_id)
    db.add(db_stable)
    db.flush()  # Получаем id

    # Автоматически создаем здание администрации (level=1)
    admin_building = Building(
        type="administration",
        level=1,
        stable_id=db_stable.id
    )
    db.add(admin_building)

    # Создаём боксы: теперь их ровно столько, каков уровень stable
    for i in range(db_stable.level):
        box = Box(name=f"Box {i+1}", stable_id=db_stable.id)
        db.add(box)

    db.commit()
    db.refresh(db_stable)
    return db_stable
