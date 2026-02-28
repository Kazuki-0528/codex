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
