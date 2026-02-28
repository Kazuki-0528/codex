from sqlalchemy.orm import Session

from . import models, schemas


def list_buildings(db: Session) -> list[models.Building]:
    return db.query(models.Building).order_by(models.Building.id.asc()).all()


def get_building(db: Session, building_id: int) -> models.Building | None:
    return db.query(models.Building).filter(models.Building.id == building_id).first()


def create_building(db: Session, payload: schemas.BuildingCreate) -> models.Building:
    building = models.Building(**payload.model_dump())
    db.add(building)
    db.commit()
    db.refresh(building)
    return building


def update_building(db: Session, building: models.Building, payload: schemas.BuildingUpdate) -> models.Building:
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(building, key, value)
    db.commit()
    db.refresh(building)
    return building
