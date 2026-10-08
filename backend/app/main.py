from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.services.db_service import init_db
from app.api import scenarios, zones, roads, resources, vehicles, hospitals, shelters, planning, ws

# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Enable CORS for Frontend Development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Database Initialization & Seeding
@app.on_event("startup")
def on_startup():
    init_db()

# Include Routers
app.include_router(scenarios.router, prefix=settings.API_V1_STR, tags=["scenarios"])
app.include_router(zones.router, prefix=settings.API_V1_STR, tags=["zones"])
app.include_router(roads.router, prefix=settings.API_V1_STR, tags=["roads"])
app.include_router(resources.router, prefix=settings.API_V1_STR, tags=["resources"])
app.include_router(vehicles.router, prefix=settings.API_V1_STR, tags=["vehicles"])
app.include_router(hospitals.router, prefix=settings.API_V1_STR, tags=["hospitals"])
app.include_router(shelters.router, prefix=settings.API_V1_STR, tags=["shelters"])
app.include_router(planning.router, prefix=settings.API_V1_STR, tags=["planning"])
app.include_router(ws.router, tags=["websockets"])

@app.get("/")
def root():
    return {
        "message": "Disaster Relief AI Resource Allocation Planner API",
        "docs_url": "/docs",
        "health": "OK"
    }
