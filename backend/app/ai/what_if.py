import copy
from typing import List
from app.schemas.schemas import (
    WhatIfRequest, WhatIfComparison, ActionPlanResult, ZoneBase, WarehouseBase,
    RoadBase, VehicleBase, TeamBase, HospitalBase, ShelterBase
)
from app.ai.planning_engine import generate_complete_action_plan

def run_what_if_simulation(
    request: WhatIfRequest,
    scenario_id: str,
    zones: List[ZoneBase],
    warehouses: List[WarehouseBase],
    roads: List[RoadBase],
    vehicles: List[VehicleBase],
    teams: List[TeamBase],
    hospitals: List[HospitalBase],
    shelters: List[ShelterBase]
) -> WhatIfComparison:
    """
    Phase 17: What-If Simulation Engine
    Allows users to modify road status, resource quantity, population, hospital beds, or zone severity,
    runs the plan, and compares simulated results against the baseline.
    """
    # 1. Generate Baseline Plan
    baseline_plan = generate_complete_action_plan(
        scenario_id, zones, warehouses, roads, vehicles, teams, hospitals, shelters
    )

    # 2. Deepcopy state and apply What-If overrides
    sim_zones = copy.deepcopy(zones)
    sim_warehouses = copy.deepcopy(warehouses)
    sim_roads = copy.deepcopy(roads)
    sim_hospitals = copy.deepcopy(hospitals)

    if request.road_blockages:
        for r in sim_roads:
            if r.id in request.road_blockages:
                r.is_blocked = request.road_blockages[r.id]

    if request.resource_delta:
        for w in sim_warehouses:
            if w.id in request.resource_delta:
                for item, delta in request.resource_delta[w.id].items():
                    w.stock[item] = max(0, w.stock.get(item, 0) + delta)

    if request.zone_severity_override:
        for z in sim_zones:
            if z.id in request.zone_severity_override:
                z.severity = request.zone_severity_override[z.id]

    if request.hospital_bed_delta:
        for h in sim_hospitals:
            if h.id in request.hospital_bed_delta:
                h.available_beds = max(0, h.available_beds + request.hospital_bed_delta[h.id])

    # 3. Generate Simulated Plan
    simulated_plan = generate_complete_action_plan(
        scenario_id, sim_zones, sim_warehouses, sim_roads, vehicles, teams, sim_hospitals, shelters
    )

    # 4. Generate Diff Summary
    base_opt = baseline_plan.optimization
    sim_opt = simulated_plan.optimization
    
    diff_summary = {
        "coverage_change_percent": round(sim_opt.critical_coverage_percentage - base_opt.critical_coverage_percentage, 2),
        "population_served_delta": sim_opt.total_population_served - base_opt.total_population_served,
        "new_violations_introduced": len(simulated_plan.validation.violations) - len(baseline_plan.validation.violations),
        "route_changes_count": sum(1 for b, s in zip(baseline_plan.routes, simulated_plan.routes) if b.path != s.path)
    }

    return WhatIfComparison(
        baseline_plan=baseline_plan,
        simulated_plan=simulated_plan,
        diff_summary=diff_summary
    )
