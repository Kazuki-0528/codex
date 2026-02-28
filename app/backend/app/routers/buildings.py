from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..db import get_db
from ..security import require_read_role, require_write_role

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("", response_model=list[schemas.BuildingRead], dependencies=[Depends(require_read_role)])
def list_buildings(db: Session = Depends(get_db)):
    return crud.list_buildings(db)


@router.post("", response_model=schemas.BuildingRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_write_role)])
def create_building(payload: schemas.BuildingCreate, db: Session = Depends(get_db)):
    return crud.create_building(db, payload)


@router.patch("/{building_id}", response_model=schemas.BuildingRead, dependencies=[Depends(require_write_role)])
def patch_building(building_id: int, payload: schemas.BuildingUpdate, db: Session = Depends(get_db)):
    building = crud.get_building(db, building_id)
    if building is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")
    return crud.update_building(db, building, payload)
