def upgrade_building(db: Session, building_id: str):
    building = db.query(Building).filter_by(id=building_id).first()
    if not building:
        raise ValueError("Building not found")

    stable = building.stable

    # Проверка: нельзя апнуть выше уровня stable
    if building.level >= stable.level:
        raise ValueError("Building level can't exceed stable level")

    building.level += 1
    db.commit()
    db.refresh(building)
    return building

def upgrade_stable(db: Session, stable_id: str):
    stable = db.query(Stable).filter_by(id=stable_id).first()
    if not stable:
        raise ValueError("Stable not found")

    # Каждые 5 уровней проверяем, что все здания не ниже текущих 5-уровневых порогов
    if (stable.level + 1) % 5 == 1:
        for building in stable.buildings:
            if building.type != "administration" and building.level < (stable.level // 5) * 5:
                raise ValueError("Все здания должны быть не ниже 5 уровня перед апгрейдом stable")

    stable.level += 1

    # После повышения stable увеличиваем количество боксов до нового уровня
    existing_boxes = len(stable.boxes)
    for i in range(existing_boxes, stable.level):
        box = Box(name=f"Box {i+1}", stable_id=stable.id)
        db.add(box)

    db.commit()
    db.refresh(stable)
    return stable
