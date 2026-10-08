from typing import List, Optional, Dict, Any
from app.schemas.schemas import ActionPlanResult, ZoneBase, WarehouseBase, RoadBase, VehicleBase, TeamBase, HospitalBase, ShelterBase
from app.ai.planning_engine import generate_complete_action_plan

def trigger_dynamic_replan(
    scenario_id: str,
    event_type: str,
    target_id: str,
    event_data: Dict[str, Any],
    zones: List[ZoneBase],
    warehouses: List[WarehouseBase],
    roads: List[RoadBase],
    vehicles: List[VehicleBase],
    teams: List[TeamBase],
    hospitals: List[HospitalBase],
    shelters: List[ShelterBase]
) -> ActionPlanResult:
    """
    Phase 15: Dynamic Replanning Engine
    Triggers immediate plan recalculation upon state changes (e.g. road blockage, demand spike).
    Flow: New Event -> State Mutation -> Risk -> Priority -> Routes -> Optimization -> Constraints -> New Action Plan
    """
    # 1. Mutate state based on event
    if event_type == "ROAD_BLOCKAGE":
        for r in roads:
            if r.id == target_id:
                r.is_blocked = event_data.get("is_blocked", True)
                
    elif event_type == "DEMAND_SPIKE":
        for z in zones:
            if z.id == target_id:
                z.severity = event_data.get("severity", "Critical")
                for k, v in event_data.get("critical_needs_delta", {}).items():
                    z.critical_needs[k] = max(0, z.critical_needs.get(k, 0) + v)

    elif event_type == "STOCK_DEPLETION":
        for w in warehouses:
            if w.id == target_id:
                for k, v in event_data.get("stock_delta", {}).items():
                    w.stock[k] = max(0, w.stock.get(k, 0) + v)

    # 2. Re-run complete planning pipeline
    new_plan = generate_complete_action_plan(
        scenario_id, zones, warehouses, roads, vehicles, teams, hospitals, shelters
    )
    
    return new_plan
