import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config.settings import settings
from app.models.db_models import (
    Base, ScenarioDB, ZoneDB, WarehouseDB, HospitalDB, ShelterDB,
    VehicleDB, TeamDB, RoadDB
)

# Setup Engine
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if DB is already seeded
        if db.query(ZoneDB).count() == 0:
            seed_file = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "seed_data.json")
            if os.path.exists(seed_file):
                with open(seed_file, "r") as f:
                    data = json.load(f)
                
                # Seed Scenario
                scenario = ScenarioDB(
                    id="SCENARIO-01",
                    name="Monsoon Flood Disaster Run",
                    description="Severe urban flooding across 8 zones",
                    disaster_type="Flood",
                    severity_level="Severe",
                    active=True
                )
                db.add(scenario)

                # Seed Zones
                for z in data.get("zones", []):
                    db.add(ZoneDB(**z))

                # Seed Warehouses
                for w in data.get("warehouses", []):
                    db.add(WarehouseDB(**w))

                # Seed Hospitals
                for h in data.get("hospitals", []):
                    db.add(HospitalDB(**h))

                # Seed Shelters
                for s in data.get("shelters", []):
                    db.add(ShelterDB(**s))

                # Seed Vehicles
                for v in data.get("vehicles", []):
                    db.add(VehicleDB(**v))

                # Seed Teams
                for t in data.get("teams", []):
                    db.add(TeamDB(**t))

                # Seed Roads
                for r in data.get("roads", []):
                    db.add(RoadDB(**r))

                db.commit()
    finally:
        db.close()
