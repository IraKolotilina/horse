from sqlalchemy.orm import Session
from app.models.player import Player
from app.models.building import Building
from app.schemas.player import PlayerCreate
from app.core.security import hash_password

def create_player_with_admin(db: Session, player_data: PlayerCreate) -> Player:
    existing = db.query(Player).filter(Player.username == player_data.username).first()
    if existing:
        raise ValueError("Username already taken")

    hashed_password = hash_password(player_data.password)
    new_player = Player(username=player_data.username, email=player_data.email, password=hashed_password)
    db.add(new_player)
    db.flush()

    # Создаем стартовую конюшню
    start_stable = Stable(name="Главная конюшня", owner_id=new_player.id)
    db.add(start_stable)
    db.flush()

    # Создаем здание администрации в конюшне
    admin_building = Building(type="administration", stable_id=start_stable.id, level=1)
    db.add(admin_building)

    db.commit()
    db.refresh(new_player)
    return new_player

