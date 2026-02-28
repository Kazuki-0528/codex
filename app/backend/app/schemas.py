from pydantic import BaseModel, Field


class BuildingBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    location: str = Field(min_length=2, max_length=120)
    gross_area_m2: int = Field(gt=0, le=10_000_000)


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    location: str | None = Field(default=None, min_length=2, max_length=120)
    gross_area_m2: int | None = Field(default=None, gt=0, le=10_000_000)


class BuildingRead(BuildingBase):
    id: int

    class Config:
        from_attributes = True


class IfcImportSummary(BaseModel):
    building_id: int
    building_name: str
    rooms_created: int
    walls_created: int
    windows_created: int


class RoomMonthlyEstimate(BaseModel):
    room_id: int
    room_name: str
    usage_type: str
    area_m2: float
    operating_hours_per_day: float
    estimated_monthly_kgco2: float


class BuildingMonthlyEstimate(BaseModel):
    building_id: int
    working_days_per_month: int
    total_monthly_kgco2: float
    rooms: list[RoomMonthlyEstimate]
