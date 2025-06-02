from sqlalchemy.orm import Session
from app.models.stable import Stable
from app.models.building import Building
from app.models.player import Player
from app.schemas.stable import StableCreate
from fastapi import HTTPException, status
import sqlalchemy.exc


def create_stable(db: Session, player: Player, stable_data: StableCreate) -> Stable:
    try:
        new_stable = Stable(name=stable_data.name, owner_id=player.id)
        db.add(new_stable)
        db.flush()  # Получаем ID

        admin_building = Building(
            type="administration",  # Можно заменить на константу или Enum
            level=1,
            stable_id=new_stable.id
        )
        db.add(admin_building)

        db.commit()
        db.refresh(new_stable)
        return new_stable

    except sqlalchemy.exc.SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании конюшни: {str(e)}"
        )
