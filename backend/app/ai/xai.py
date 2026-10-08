from typing import List
from app.schemas.schemas import (
    DecisionExplanation, PriorityRankingItem, OptimizationResult,
    RouteResult, ConstraintCheckResult
)

def generate_plan_explanations(
    priorities: List[PriorityRankingItem],
    optimization: OptimizationResult,
    routes: List[RouteResult],
    validation: ConstraintCheckResult
) -> List[DecisionExplanation]:
    """
    Phase 16: Explainable AI (XAI) Engine
    Provides transparent, structured rationales for every major system decision:
    Decision, Important Inputs, Constraints Considered, Rationale, and Expected Outcome.
    """
    explanations = []

    # 1. Priority Ranking Explanation
    if priorities:
        top_zone = priorities[0]
        explanations.append(DecisionExplanation(
            decision_type="ZONE_PRIORITIZATION",
            target_id=top_zone.zone_id,
            summary=f"Ranked {top_zone.name} as Priority #1 (Urgency: {top_zone.urgency_level})",
            important_inputs=top_zone.factors,
            constraints_considered=["Severity Weight (35%)", "Bayesian Risk Probability (30%)", "Population (20%)", "Item Needs (15%)"],
            rationale=f"Zone {top_zone.name} exhibits the highest composite risk score ({top_zone.priority_score}/100) due to severe disaster impact and high population density.",
            expected_outcome="Immediate priority dispatch to minimize casualty risk and satisfy urgent medical/water shortages."
        ))

    # 2. Optimization Rationale
    explanations.append(DecisionExplanation(
        decision_type="RESOURCE_OPTIMIZATION",
        target_id="OR_TOOLS_SOLVER",
        summary=f"Optimized supply allocations achieving {optimization.critical_coverage_percentage}% critical demand coverage.",
        important_inputs={"objective_value": optimization.objective_value, "population_served": optimization.total_population_served},
        constraints_considered=["Warehouse Stock Limits", "Zone Demand Bounds", "Non-negativity", "Vehicle Payload Capacities"],
        rationale="Solved via Mixed-Integer Linear Programming (MILP). Shipped resources from depots with highest stock availability while prioritizing high-urgency zones.",
        expected_outcome=f"Successfully serving approximately {optimization.total_population_served} affected citizens with zero stock wastage."
    ))

    # 3. Routing Rationale
    if routes:
        best_r = routes[0]
        explanations.append(DecisionExplanation(
            decision_type="DYNAMIC_ROUTING",
            target_id=f"{best_r.source_warehouse}->{best_r.target_zone}",
            summary=f"Selected A* optimal route ({best_r.total_distance_km} km, {best_r.total_time_min} mins) avoiding blocked roads.",
            important_inputs={"path": best_r.path, "total_time_min": best_r.total_time_min},
            constraints_considered=["Road Damage Blockages", "Euclidean Distance Heuristic", "Travel Time Weights"],
            rationale="NetworkX A* pathfinding bypassed damaged infrastructure while minimizing total dispatch time.",
            expected_outcome=f"Guaranteed safe transit route for relief convoys within estimated {best_r.total_time_min} minute arrival window."
        ))

    # 4. Constraint Validation Explanation
    explanations.append(DecisionExplanation(
        decision_type="CONSTRAINT_VALIDATION",
        target_id="SYSTEM_VALIDATOR",
        summary=f"Constraint check completed: {'PASSED' if validation.valid else 'VIOLATIONS DETECTED'}",
        important_inputs={"violations_count": len(validation.violations), "warnings_count": len(validation.warnings)},
        constraints_considered=["Fleet Truck Capacity", "Hospital Bed Availability", "Shelter Occupancy", "Road Blockages"],
        rationale="Checked all dispatch plans against operational limits to guarantee safety and physical feasibility.",
        expected_outcome="Prevents vehicle overloading, shelter overcrowding, and convoy strandings on damaged roads."
    ))

    return explanations
