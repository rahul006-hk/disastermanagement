from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.db_service import get_db
from app.models.db_models import (
    ZoneDB, WarehouseDB, RoadDB, VehicleDB, TeamDB, HospitalDB, ShelterDB
)
from app.schemas.schemas import (
    ActionPlanResult, WhatIfRequest, WhatIfComparison, EvaluationMetrics,
    ZoneBase, WarehouseBase, RoadBase, VehicleBase, TeamBase, HospitalBase, ShelterBase
)
from app.ai.planning_engine import generate_complete_action_plan
from app.ai.what_if import run_what_if_simulation
from app.ai.evaluation import evaluate_baselines_vs_proposed

router = APIRouter()

def _load_domain_entities(db: Session):
    zones = [ZoneBase(**z.__dict__) for z in db.query(ZoneDB).all()]
    warehouses = [WarehouseBase(**w.__dict__) for w in db.query(WarehouseDB).all()]
    roads = [RoadBase(**r.__dict__) for r in db.query(RoadDB).all()]
    vehicles = [VehicleBase(**v.__dict__) for v in db.query(VehicleDB).all()]
    teams = [TeamBase(**t.__dict__) for t in db.query(TeamDB).all()]
    hospitals = [HospitalBase(**h.__dict__) for h in db.query(HospitalDB).all()]
    shelters = [ShelterBase(**s.__dict__) for s in db.query(ShelterDB).all()]
    return zones, warehouses, roads, vehicles, teams, hospitals, shelters

@router.post("/planning/generate", response_model=ActionPlanResult)
def generate_action_plan(scenario_id: str = "SCENARIO-01", db: Session = Depends(get_db)):
    entities = _load_domain_entities(db)
    plan = generate_complete_action_plan(scenario_id, *entities)
    return plan

@router.post("/planning/what-if", response_model=WhatIfComparison)
def run_what_if(request: WhatIfRequest, scenario_id: str = "SCENARIO-01", db: Session = Depends(get_db)):
    entities = _load_domain_entities(db)
    comparison = run_what_if_simulation(request, scenario_id, *entities)
    return comparison

@router.get("/planning/evaluation", response_model=list[EvaluationMetrics])
def evaluate_benchmarks(scenario_id: str = "SCENARIO-01", db: Session = Depends(get_db)):
    entities = _load_domain_entities(db)
    proposed_plan = generate_complete_action_plan(scenario_id, *entities)
    zones, warehouses, roads, vehicles = entities[0], entities[1], entities[2], entities[3]
    eval_results = evaluate_baselines_vs_proposed(zones, warehouses, roads, vehicles, proposed_plan)
    return eval_results
