from typing import List, Dict
from app.schemas.schemas import SituationAssessment, ZoneBase, RoadBase

def calculate_situation_assessment(zones: List[ZoneBase], roads: List[RoadBase]) -> SituationAssessment:
    """
    Phase 7: Situation Assessment
    Calculates overall severity index, affected population totals, itemized critical needs,
    and identifies high urgency zones and infrastructure risk scores.
    """
    total_pop = sum(z.population for z in zones)
    
    # Severity numeric map
    sev_map = {"Critical": 1.0, "High": 0.75, "Medium": 0.5, "Low": 0.25}
    
    total_weighted_severity = sum(z.population * sev_map.get(z.severity, 0.5) for z in zones)
    overall_severity_index = round(total_weighted_severity / max(1, total_pop), 3)
    
    # Itemized needs summation
    critical_demands: Dict[str, int] = {}
    for z in zones:
        for item, qty in z.critical_needs.items():
            critical_demands[item] = critical_demands.get(item, 0) + qty
            
    # High urgency zone IDs
    high_urgency_zones = [z.id for z in zones if z.severity in ["Critical", "High"]]
    
    # Infrastructure risk score based on road blockages
    blocked_count = sum(1 for r in roads if r.is_blocked)
    total_roads = max(1, len(roads))
    infrastructure_risk_score = round(blocked_count / total_roads, 3)
    
    return SituationAssessment(
        overall_severity_index=overall_severity_index,
        affected_population_total=total_pop,
        critical_item_demands=critical_demands,
        high_urgency_zone_ids=high_urgency_zones,
        infrastructure_risk_score=infrastructure_risk_score
    )
