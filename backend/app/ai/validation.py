from typing import List, Dict
from app.schemas.schemas import (
    ConstraintCheckResult, ZoneBase, WarehouseBase, VehicleBase,
    HospitalBase, ShelterBase, AllocationItem, RouteResult
)

def validate_action_plan_constraints(
    zones: List[ZoneBase],
    warehouses: List[WarehouseBase],
    vehicles: List[VehicleBase],
    hospitals: List[HospitalBase],
    shelters: List[ShelterBase],
    allocations: List[AllocationItem],
    routes: List[RouteResult]
) -> ConstraintCheckResult:
    """
    Phase 12: Constraint Validation Engine
    Validates supply stock, vehicle payload capacity, hospital bed availability,
    shelter occupancy limits, and route blockages.
    Returns: { valid: bool, violations: List[str], warnings: List[str] }
    """
    violations = []
    warnings = []
    
    # 1. Warehouse Stock Validation
    warehouse_stock = {w.id: dict(w.stock) for w in warehouses}
    for alloc in allocations:
        w_id = alloc.warehouse_id
        if w_id not in warehouse_stock:
            violations.append(f"Allocation references non-existent warehouse {w_id}")
            continue
            
        for item, qty in alloc.resources_allocated.items():
            if warehouse_stock[w_id].get(item, 0) < qty:
                violations.append(
                    f"Warehouse {w_id} stock deficit for '{item}': required {qty}, available {warehouse_stock[w_id].get(item, 0)}"
                )
            else:
                warehouse_stock[w_id][item] -= qty

    # 2. Vehicle Capacity & Payload Validation
    trucks = [v for v in vehicles if v.type == "relief truck" and v.status == "Available"]
    total_truck_capacity = sum(v.capacity for v in trucks)
    total_shipped_units = sum(
        sum(alloc.resources_allocated.values()) for alloc in allocations
    )
    
    if total_shipped_units > total_truck_capacity:
        violations.append(
            f"Relief truck capacity exceeded: Total payload {total_shipped_units} exceeds total truck capacity {total_truck_capacity}"
        )
    elif total_shipped_units > (total_truck_capacity * 0.85):
        warnings.append(
            f"High fleet utilization: Total payload {total_shipped_units} is at {round((total_shipped_units/total_truck_capacity)*100, 1)}% capacity"
        )

    # 3. Route Availability & Blocked Road Validation
    for r_res in routes:
        for step in r_res.steps:
            if step.is_blocked:
                violations.append(
                    f"Invalid Route: Step from {step.from_node} to {step.to_node} uses blocked road"
                )

    # 4. Hospital Capacity & Bed Limit Check
    for h in hospitals:
        if h.incoming_patients > h.available_beds:
            warnings.append(
                f"Hospital {h.name} ({h.id}) bed overflow warning: {h.incoming_patients} incoming vs {h.available_beds} available beds"
            )

    # 5. Shelter Occupancy Check
    for s in shelters:
        if s.occupancy > s.capacity:
            violations.append(
                f"Shelter {s.name} ({s.id}) capacity exceeded: Occupancy {s.occupancy} > Capacity {s.capacity}"
            )
        elif s.occupancy > (s.capacity * 0.9):
            warnings.append(
                f"Shelter {s.name} ({s.id}) near max capacity ({s.occupancy}/{s.capacity})"
            )

    is_valid = len(violations) == 0
    return ConstraintCheckResult(
        valid=is_valid,
        violations=violations,
        warnings=warnings
    )
