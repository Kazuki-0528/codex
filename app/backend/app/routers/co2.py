from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..db import get_db
from ..security import require_read_role

router = APIRouter(prefix="/api/v1/co2", tags=["co2"])


@router.get("/monthly", response_model=schemas.BuildingMonthlyEstimate, dependencies=[Depends(require_read_role)])
def estimate_monthly_co2(
    building_id: int = Query(gt=0),
    working_days_per_month: int = Query(default=22, ge=1, le=31),
    db: Session = Depends(get_db),
):
    try:
        return crud.estimate_building_monthly_co2(
            db=db,
            building_id=building_id,
            working_days_per_month=working_days_per_month,
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
