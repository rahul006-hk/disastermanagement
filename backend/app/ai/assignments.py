from typing import List, Dict, Any
from app.schemas.schemas import (
    VehicleBase, HospitalBase, ShelterBase, ZoneBase, AllocationItem, RouteResult
)

def generate_entity_assignments(
    zones: List[ZoneBase],
    vehicles: List[VehicleBase],
    hospitals: List[HospitalBase],
    shelters: List[ShelterBase],
    allocations: List[AllocationItem],
    routes: List[RouteResult]
) -> Dict[str, Any]:
    """
    Phase 14: Vehicle, Hospital, and Shelter Assignments Engine
    - Vehicle: ambulance -> medical; relief truck -> supplies; rescue vehicle -> rescue teams
    - Hospital: bed capacity, emergency capability & routing distance
    - Shelter: capacity, accessibility & facilities
    """
    vehicle_assignments = []
    hospital_assignments = []
    shelter_assignments = []

    # 1. Vehicle Dispatch Assignments based on allocations
    truck_idx = 0
    relief_trucks = [v for v in vehicles if v.type == "relief truck"]
    
    for alloc in allocations:
        if sum(alloc.resources_allocated.values()) > 0:
            assigned_v = relief_trucks[truck_idx % max(1, len(relief_trucks))]
            truck_idx += 1
            vehicle_assignments.append({
                "vehicle_id": assigned_v.id,
                "vehicle_name": assigned_v.name,
                "type": assigned_v.type,
                "origin_warehouse": alloc.warehouse_id,
                "target_zone": alloc.zone_id,
                "payload": alloc.resources_allocated,
                "status": "DISPATCHED"
            })

    # 2. Hospital Patient Assignments
    ambulances = [v for v in vehicles if v.type == "ambulance"]
    amb_idx = 0
    critical_zones = [z for z in zones if z.severity in ["Critical", "High"]]
    avail_hospitals = [h for h in hospitals if h.available_beds > h.incoming_patients]
    
    for z in critical_zones:
        if avail_hospitals:
            # Pick best hospital with emergency capability
            best_h = next((h for h in avail_hospitals if h.emergency_capability), avail_hospitals[0])
            patients_to_transfer = min(15, z.critical_needs.get("medicine", 100) // 10)
            amb = ambulances[amb_idx % max(1, len(ambulances))]
            amb_idx += 1
            
            hospital_assignments.append({
                "source_zone_id": z.id,
                "source_zone_name": z.name,
                "hospital_id": best_h.id,
                "hospital_name": best_h.name,
                "assigned_ambulance": amb.id,
                "patients_transferred": patients_to_transfer,
                "hospital_remaining_beds": max(0, best_h.available_beds - best_h.incoming_patients - patients_to_transfer)
            })

    # 3. Shelter Evacuation Assignments
    high_pop_zones = sorted(zones, key=lambda x: x.population, reverse=True)[:4]
    avail_shelters = [s for s in shelters if s.occupancy < s.capacity]
    
    for idx, z in enumerate(high_pop_zones):
        if avail_shelters:
            target_s = avail_shelters[idx % len(avail_shelters)]
            evacuees = min(200, target_s.capacity - target_s.occupancy)
            shelter_assignments.append({
                "source_zone_id": z.id,
                "source_zone_name": z.name,
                "shelter_id": target_s.id,
                "shelter_name": target_s.name,
                "evacuees_assigned": evacuees,
                "facilities_available": target_s.facilities,
                "accessibility": target_s.accessibility
            })

    return {
        "vehicles": vehicle_assignments,
        "hospitals": hospital_assignments,
        "shelters": shelter_assignments
    }
