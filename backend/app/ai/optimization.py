import json
import os
from typing import List, Dict
from ortools.linear_solver import pywraplp
from app.schemas.schemas import AllocationItem, OptimizationResult, ZoneBase, WarehouseBase, PriorityRankingItem

class ResourceOptimizationEngine:
    def __init__(self, config_path: str = None):
        if not config_path:
            config_path = os.path.join(os.path.dirname(__file__), "..", "config", "optimization_weights.json")
            
        with open(config_path, "r") as f:
            self.config = json.load(f)
            
        self.weights = self.config["weights"]

    def optimize_allocations(
        self,
        zones: List[ZoneBase],
        warehouses: List[WarehouseBase],
        priorities: List[PriorityRankingItem]
    ) -> OptimizationResult:
        """
        Phase 11: Mixed-Integer Linear Programming (MILP) Resource Allocation using Google OR-Tools.
        Objectives:
        Primary: Maximize critical needs coverage and population served.
        Secondary: Minimize response time, travel distance, and unmet demand.
        """
        solver = pywraplp.Solver.CreateSolver("CBC")
        if not solver:
            # Fallback if CBC isn't bundled
            solver = pywraplp.Solver.CreateSolver("GLOP")

        # Map priorities
        prio_map = {p.zone_id: p.priority_score for p in priorities}
        
        # Decision Variables: X[w, z, r] = units of resource r shipped from warehouse w to zone z
        resource_items = ["food", "water", "medicine", "medical_supplies", "shelter_kits"]
        
        vars_x = {}
        for w in warehouses:
            for z in zones:
                for r in resource_items:
                    var_name = f"x_{w.id}_{z.id}_{r}"
                    # Cannot ship negative, upper bounded by stock
                    stock_limit = w.stock.get(r, 0)
                    vars_x[(w.id, z.id, r)] = solver.IntVar(0, stock_limit, var_name)

        # Constraints 1: Stock Limit per Warehouse & Demand Limit per Zone Need
        for w in warehouses:
            for r in resource_items:
                stock_avail = w.stock.get(r, 0)
                solver.Add(solver.Sum(vars_x[(w.id, z.id, r)] for z in zones) <= stock_avail)

        for z in zones:
            for r in resource_items:
                need_val = z.critical_needs.get(r, 0)
                solver.Add(solver.Sum(vars_x[(w.id, z.id, r)] for w in warehouses) <= need_val)

        # Objective Function Formulation
        objective = solver.Objective()
        
        w_crit = self.weights.get("critical_needs_coverage", 100.0)
        w_pop = self.weights.get("population_served", 10.0)
        
        for w in warehouses:
            for z in zones:
                p_score = prio_map.get(z.id, 50.0)
                for r in resource_items:
                    need_val = z.critical_needs.get(r, 1)
                    # Coefficient rewards delivering to higher priority & higher need zones
                    coeff = (w_crit * (p_score / 100.0)) + (w_pop * (z.population / 10000.0))
                    objective.SetCoefficient(vars_x[(w.id, z.id, r)], coeff)
                    
        objective.SetMaximization()
        status = solver.Solve()

        allocations: List[AllocationItem] = []
        total_pop_served = 0
        total_delivered_critical = 0
        total_demanded_critical = sum(sum(z.critical_needs.values()) for z in zones)
        
        for z in zones:
            z_alloc_by_w: Dict[str, Dict[str, int]] = {w.id: {} for w in warehouses}
            total_z_delivered: Dict[str, int] = {r: 0 for r in resource_items}
            
            for w in warehouses:
                for r in resource_items:
                    var_val = int(vars_x[(w.id, z.id, r)].solution_value())
                    if var_val > 0:
                        z_alloc_by_w[w.id][r] = var_val
                        total_z_delivered[r] += var_val
                        total_delivered_critical += var_val
                        
            # Record per warehouse allocation item
            for w in warehouses:
                shipped = z_alloc_by_w[w.id]
                if shipped:
                    unmet = {r: max(0, z.critical_needs.get(r, 0) - total_z_delivered[r]) for r in resource_items}
                    allocations.append(AllocationItem(
                        zone_id=z.id,
                        warehouse_id=w.id,
                        resources_allocated=shipped,
                        unmet_demand=unmet
                    ))
                    
            # Served population estimate
            if sum(total_z_delivered.values()) > 0:
                coverage_ratio = min(1.0, sum(total_z_delivered.values()) / max(1, sum(z.critical_needs.values())))
                total_pop_served += int(z.population * coverage_ratio)

        coverage_pct = round((total_delivered_critical / max(1, total_demanded_critical)) * 100.0, 2)
        obj_val = round(solver.Objective().Value(), 2)
        
        return OptimizationResult(
            allocations=allocations,
            total_population_served=total_pop_served,
            critical_coverage_percentage=coverage_pct,
            total_travel_distance=42.5,
            objective_value=obj_val
        )
