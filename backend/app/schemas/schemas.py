from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

# Base Schemas
class ZoneBase(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    population: int
    severity: str
    critical_needs: Dict[str, int]

class WarehouseBase(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    stock: Dict[str, int]

class HospitalBase(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    capacity: int
    available_beds: int
    emergency_capability: bool
    incoming_patients: int

class ShelterBase(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    capacity: int
    occupancy: int
    facilities: List[str]
    accessibility: str

class VehicleBase(BaseModel):
    id: str
    name: str
    type: str
    capacity: int
    assigned_warehouse: Optional[str] = None
    status: str = "Available"

class TeamBase(BaseModel):
    id: str
    name: str
    type: str
    members: int
    status: str = "Ready"

class RoadBase(BaseModel):
    id: str
    source: str
    target: str
    distance_km: float
    travel_time_min: float
    is_blocked: bool = False

class RoadUpdate(BaseModel):
    is_blocked: bool

class ScenarioCreate(BaseModel):
    name: str = "Disaster Relief Run"
    description: str = "Flood impact scenario"
    disaster_type: str = "Flood"
    severity_level: str = "Severe"

class SituationAssessment(BaseModel):
    overall_severity_index: float
    affected_population_total: int
    critical_item_demands: Dict[str, int]
    high_urgency_zone_ids: List[str]
    infrastructure_risk_score: float

class BayesianRiskResult(BaseModel):
    zone_risks: Dict[str, float]
    risk_factors: Dict[str, Dict[str, Any]]
    evidence_used: Dict[str, str]

class PriorityRankingItem(BaseModel):
    zone_id: str
    name: str
    rank: int
    priority_score: float
    urgency_level: str
    factors: Dict[str, Any]

class RouteStep(BaseModel):
    from_node: str
    to_node: str
    distance_km: float
    time_min: float
    is_blocked: bool = False

class RouteResult(BaseModel):
    source_warehouse: str
    target_zone: str
    path: List[str]
    total_distance_km: float
    total_time_min: float
    steps: List[RouteStep]

class AllocationItem(BaseModel):
    zone_id: str
    warehouse_id: str
    resources_allocated: Dict[str, int]
    unmet_demand: Dict[str, int]

class OptimizationResult(BaseModel):
    allocations: List[AllocationItem]
    total_population_served: int
    critical_coverage_percentage: float
    total_travel_distance: float
    objective_value: float

class ConstraintCheckResult(BaseModel):
    valid: bool
    violations: List[str]
    warnings: List[str]

class DecisionExplanation(BaseModel):
    decision_type: str
    target_id: str
    summary: str
    important_inputs: Dict[str, Any]
    constraints_considered: List[str]
    rationale: str
    expected_outcome: str

class ActionPlanResult(BaseModel):
    scenario_id: str
    assessment: SituationAssessment
    bayesian_risk: BayesianRiskResult
    priorities: List[PriorityRankingItem]
    routes: List[RouteResult]
    optimization: OptimizationResult
    validation: ConstraintCheckResult
    assignments: Dict[str, Any]
    explanations: List[DecisionExplanation]

class WhatIfRequest(BaseModel):
    road_blockages: Optional[Dict[str, bool]] = None  # road_id -> is_blocked
    resource_delta: Optional[Dict[str, Dict[str, int]]] = None  # warehouse_id -> {food: -500}
    zone_severity_override: Optional[Dict[str, str]] = None  # zone_id -> "Critical"
    hospital_bed_delta: Optional[Dict[str, int]] = None  # hospital_id -> available_beds

class WhatIfComparison(BaseModel):
    baseline_plan: ActionPlanResult
    simulated_plan: ActionPlanResult
    diff_summary: Dict[str, Any]

class EvaluationMetrics(BaseModel):
    planner_name: str
    population_served: int
    critical_demand_coverage_percent: float
    avg_response_time_min: float
    total_travel_distance_km: float
    unmet_critical_items: int
    constraint_violations: int
    assignment_success_rate_percent: float
