from fastapi import FastAPI

from .routers import buildings, co2, health, imports

app = FastAPI(title="FM Portfolio API", version="0.1.0")

app.include_router(health.router)
app.include_router(buildings.router, prefix="/api/v1")
app.include_router(imports.router)
app.include_router(co2.router)
