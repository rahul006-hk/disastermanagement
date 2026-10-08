from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.db_service import get_db
from app.models.db_models import ScenarioDB, ZoneDB, RoadDB
from app.schemas.schemas import ScenarioCreate
from app.simulation.scenario_simulator import DisasterScenarioSimulator
from app.schemas.schemas import ZoneBase, RoadBase

router = APIRouter()

@router.get("/scenarios")
def get_scenarios(db: Session = Depends(get_db)):
    return db.query(ScenarioDB).all()

@router.post("/scenarios/simulate")
def run_scenario_simulation(ticks: int = 15, db: Session = Depends(get_db)):
    zones_db = db.query(ZoneDB).all()
    roads_db = db.query(RoadDB).all()
    
    zones = [ZoneBase(**z.__dict__) for z in zones_db]
    roads = [RoadBase(**r.__dict__) for r in roads_db]
    
    simulator = DisasterScenarioSimulator(zones, roads)
    events = simulator.run_simulation(total_ticks=ticks)
    
    # Save road updates back to DB
    for r in roads:
        db_road = db.query(RoadDB).filter(RoadDB.id == r.id).first()
        if db_road:
            db_road.is_blocked = r.is_blocked
    db.commit()
    
    return {"status": "SUCCESS", "ticks_simulated": ticks, "events_generated": events}
