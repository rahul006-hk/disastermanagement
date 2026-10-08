from app.services.db_service import init_db, SessionLocal
from app.models.db_models import (
    ZoneDB, WarehouseDB, RoadDB, VehicleDB, TeamDB, HospitalDB, ShelterDB
)
from app.schemas.schemas import (
    ZoneBase, WarehouseBase, RoadBase, VehicleBase, TeamBase, HospitalBase, ShelterBase
)
from app.ai.planning_engine import generate_complete_action_plan

def test_full_action_planning_pipeline():
    init_db()
    db = SessionLocal()
    try:
        zones = [ZoneBase(**z.__dict__) for z in db.query(ZoneDB).all()]
        warehouses = [WarehouseBase(**w.__dict__) for w in db.query(WarehouseDB).all()]
        roads = [RoadBase(**r.__dict__) for r in db.query(RoadDB).all()]
        vehicles = [VehicleBase(**v.__dict__) for v in db.query(VehicleDB).all()]
        teams = [TeamBase(**t.__dict__) for t in db.query(TeamDB).all()]
        hospitals = [HospitalBase(**h.__dict__) for h in db.query(HospitalDB).all()]
        shelters = [ShelterBase(**s.__dict__) for s in db.query(ShelterDB).all()]

        plan = generate_complete_action_plan(
            "TEST-SCENARIO", zones, warehouses, roads, vehicles, teams, hospitals, shelters
        )

        assert plan.scenario_id == "TEST-SCENARIO"
        assert plan.assessment.overall_severity_index > 0.0
        assert len(plan.priorities) == 8
        assert plan.optimization.critical_coverage_percentage > 0.0
        assert len(plan.explanations) >= 4
    finally:
        db.close()
