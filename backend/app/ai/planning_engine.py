from typing import List
from app.schemas.schemas import ActionPlanResult, ZoneBase, WarehouseBase, RoadBase, VehicleBase, TeamBase, HospitalBase, ShelterBase
from app.ai.assessment import calculate_situation_assessment
from app.ai.bayesian import BayesianRiskEngine
from app.ai.priority import rank_zones_by_priority
from app.ai.routing import DynamicRoutingEngine
from app.ai.optimization import ResourceOptimizationEngine
from app.ai.validation import validate_action_plan_constraints
from app.ai.assignments import generate_entity_assignments
from app.ai.xai import generate_plan_explanations

def generate_complete_action_plan(
    scenario_id: str,
    zones: List[ZoneBase],
    warehouses: List[WarehouseBase],
    roads: List[RoadBase],
    vehicles: List[VehicleBase],
    teams: List[TeamBase],
    hospitals: List[HospitalBase],
    shelters: List[ShelterBase]
) -> ActionPlanResult:
    """
    Phase 13: End-to-End Automated Action Planner
    Integrates all core AI/Optimization engines into a single executable dispatch plan.
    """
    # 1. Situation Assessment
    assessment = calculate_situation_assessment(zones, roads)

    # 2. Bayesian Risk Prediction
    bayes_engine = BayesianRiskEngine()
    bayesian_risk = bayes_engine.evaluate_zone_risks(zones, rainfall_evidence="High")

    # 3. Priority Ranking
    priorities = rank_zones_by_priority(zones, assessment, bayesian_risk)

    # 4. A* Dynamic Routing
    nodes_geo = {}
    for z in zones:
        nodes_geo[z.id] = (z.lat, z.lng)
    for w in warehouses:
        nodes_geo[w.id] = (w.lat, w.lng)
    for h in hospitals:
        nodes_geo[h.id] = (h.lat, h.lng)
    for s in shelters:
        nodes_geo[s.id] = (s.lat, s.lng)

    router = DynamicRoutingEngine(roads, nodes_geo)
    routes = []
    for prio in priorities[:4]:  # Top 4 priority zones
        for w in warehouses:
            r = router.find_best_route(w.id, prio.zone_id)
            if r:
                routes.append(r)

    # 5. OR-Tools Resource Optimization
    opt_engine = ResourceOptimizationEngine()
    optimization = opt_engine.optimize_allocations(zones, warehouses, priorities)

    # 6. Constraint Validation
    validation = validate_action_plan_constraints(
        zones, warehouses, vehicles, hospitals, shelters,
        optimization.allocations, routes
    )

    # 7. Assignments (Vehicles, Hospitals, Shelters)
    assignments = generate_entity_assignments(
        zones, vehicles, hospitals, shelters, optimization.allocations, routes
    )

    # 8. Explainable AI (XAI)
    explanations = generate_plan_explanations(priorities, optimization, routes, validation)

    return ActionPlanResult(
        scenario_id=scenario_id,
        assessment=assessment,
        bayesian_risk=bayesian_risk,
        priorities=priorities,
        routes=routes,
        optimization=optimization,
        validation=validation,
        assignments=assignments,
        explanations=explanations
    )
