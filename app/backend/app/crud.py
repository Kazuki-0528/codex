from sqlalchemy.orm import Session

from . import models, schemas
from .co2_estimator import estimate_monthly_co2_kg
from .ifcxml_parser import ParsedIfcModel


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


def _infer_usage_type(room_name: str) -> str:
    lowered = room_name.lower()
    if "meeting" in lowered:
        return "meeting"
    if "storage" in lowered:
        return "storage"
    if "corridor" in lowered:
        return "corridor"
    return "office"


def import_ifc_model(db: Session, parsed: ParsedIfcModel) -> schemas.IfcImportSummary:
    building = models.Building(name=parsed.building_name[:120], location="Unknown", gross_area_m2=1)
    db.add(building)
    db.flush()

    for space in parsed.spaces:
        db.add(
            models.Room(
                building_id=building.id,
                ifc_id=space.ifc_id,
                name=space.name[:120],
                usage_type=_infer_usage_type(space.name),
                area_m2=30.0,
                operating_hours_per_day=8.0,
            )
        )

    for wall in parsed.walls:
        db.add(
            models.EnvelopeElement(
                building_id=building.id,
                ifc_id=wall.ifc_id,
                element_type="IfcWallStandardCase",
                name=wall.name[:120],
            )
        )

    for window in parsed.windows:
        db.add(
            models.EnvelopeElement(
                building_id=building.id,
                ifc_id=window.ifc_id,
                element_type="IfcWindow",
                name=window.name[:120],
            )
        )

    db.commit()

    return schemas.IfcImportSummary(
        building_id=building.id,
        building_name=building.name,
        rooms_created=len(parsed.spaces),
        walls_created=len(parsed.walls),
        windows_created=len(parsed.windows),
    )


def estimate_building_monthly_co2(
    db: Session,
    building_id: int,
    working_days_per_month: int,
) -> schemas.BuildingMonthlyEstimate:
    building = get_building(db, building_id)
    if building is None:
        raise ValueError("Building not found")

    rooms = db.query(models.Room).filter(models.Room.building_id == building_id).order_by(models.Room.id.asc()).all()

    estimates: list[schemas.RoomMonthlyEstimate] = []
    total = 0.0
    for room in rooms:
        estimated = estimate_monthly_co2_kg(
            usage_type=room.usage_type,
            area_m2=room.area_m2,
            operating_hours_per_day=room.operating_hours_per_day,
            working_days_per_month=working_days_per_month,
        )
        total += estimated
        estimates.append(
            schemas.RoomMonthlyEstimate(
                room_id=room.id,
                room_name=room.name,
                usage_type=room.usage_type,
                area_m2=room.area_m2,
                operating_hours_per_day=room.operating_hours_per_day,
                estimated_monthly_kgco2=estimated,
            )
        )

    return schemas.BuildingMonthlyEstimate(
        building_id=building_id,
        working_days_per_month=working_days_per_month,
        total_monthly_kgco2=round(total, 3),
        rooms=estimates,
    )
