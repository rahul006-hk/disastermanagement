export interface Zone {
  id: string;
  name: string;
  lat: number;
  lng: number;
  population: number;
  severity: "Critical" | "High" | "Medium" | "Low";
  critical_needs: Record<string, number>;
}

export interface Warehouse {
  id: string;
  name: string;
  lat: number;
  lng: number;
  stock: Record<string, number>;
}

export interface Hospital {
  id: string;
  name: string;
  lat: number;
  lng: number;
  capacity: number;
  available_beds: number;
  emergency_capability: boolean;
  incoming_patients: number;
}

export interface Shelter {
  id: string;
  name: string;
  lat: number;
  lng: number;
  capacity: number;
  occupancy: number;
  facilities: string[];
  accessibility: string;
}

export interface Vehicle {
  id: string;
  name: string;
  type: string;
  capacity: number;
  assigned_warehouse?: string;
  status: string;
}

export interface Road {
  id: string;
  source: string;
  target: string;
  distance_km: number;
  travel_time_min: number;
  is_blocked: boolean;
}

export interface SituationAssessment {
  overall_severity_index: number;
  affected_population_total: number;
  critical_item_demands: Record<string, number>;
  high_urgency_zone_ids: string[];
  infrastructure_risk_score: number;
}

export interface BayesianRiskResult {
  zone_risks: Record<string, number>;
  risk_factors: Record<string, Record<string, any>>;
  evidence_used: Record<string, string>;
}

export interface PriorityRankingItem {
  zone_id: string;
  name: string;
  rank: number;
  priority_score: number;
  urgency_level: string;
  factors: Record<string, any>;
}

export interface RouteStep {
  from_node: string;
  to_node: string;
  distance_km: number;
  time_min: number;
  is_blocked: boolean;
}

export interface RouteResult {
  source_warehouse: string;
  target_zone: string;
  path: string[];
  total_distance_km: number;
  total_time_min: number;
  steps: RouteStep[];
}

export interface AllocationItem {
  zone_id: string;
  warehouse_id: string;
  resources_allocated: Record<string, number>;
  unmet_demand: Record<string, number>;
}

export interface OptimizationResult {
  allocations: AllocationItem[];
  total_population_served: number;
  critical_coverage_percentage: number;
  total_travel_distance: number;
  objective_value: number;
}

export interface ConstraintCheckResult {
  valid: boolean;
  violations: string[];
  warnings: string[];
}

export interface DecisionExplanation {
  decision_type: string;
  target_id: string;
  summary: string;
  important_inputs: Record<string, any>;
  constraints_considered: string[];
  rationale: string;
  expected_outcome: string;
}

export interface ActionPlanResult {
  scenario_id: string;
  assessment: SituationAssessment;
  bayesian_risk: BayesianRiskResult;
  priorities: PriorityRankingItem[];
  routes: RouteResult[];
  optimization: OptimizationResult;
  validation: ConstraintCheckResult;
  assignments: {
    vehicles: any[];
    hospitals: any[];
    shelters: any[];
  };
  explanations: DecisionExplanation[];
}

export interface EvaluationMetrics {
  planner_name: string;
  population_served: number;
  critical_demand_coverage_percent: number;
  avg_response_time_min: number;
  total_travel_distance_km: number;
  unmet_critical_items: number;
  constraint_violations: number;
  assignment_success_rate_percent: number;
}
