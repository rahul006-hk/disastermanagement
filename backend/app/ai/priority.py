from typing import List
from app.schemas.schemas import PriorityRankingItem, ZoneBase, SituationAssessment, BayesianRiskResult

def rank_zones_by_priority(
    zones: List[ZoneBase],
    assessment: SituationAssessment,
    bayesian_risk: BayesianRiskResult
) -> List[PriorityRankingItem]:
    """
    Phase 9: Priority Ranking Engine
    Ranks zones based on severity weight, population size, critical need volume, and Bayesian risk probability.
    """
    sev_weights = {"Critical": 4.0, "High": 3.0, "Medium": 2.0, "Low": 1.0}
    
    scored_zones = []
    for z in zones:
        sev_w = sev_weights.get(z.severity, 2.0)
        bayes_r = bayesian_risk.zone_risks.get(z.id, 0.5)
        total_items_needed = sum(z.critical_needs.values())
        
        # Priority Score Formula: (Severity * 0.35) + (BayesRisk * 0.30) + (PopLog * 0.20) + (NeedsLog * 0.15)
        # Normalized score 0 - 100
        pop_factor = min(1.0, z.population / 15000.0)
        need_factor = min(1.0, total_items_needed / 4000.0)
        
        raw_score = (sev_w / 4.0 * 35.0) + (bayes_r * 30.0) + (pop_factor * 20.0) + (need_factor * 15.0)
        priority_score = round(raw_score, 2)
        
        if priority_score >= 75.0:
            urgency_level = "CRITICAL_IMMEDIATE"
        elif priority_score >= 55.0:
            urgency_level = "HIGH_PRIORITY"
        elif priority_score >= 35.0:
            urgency_level = "MEDIUM_PRIORITY"
        else:
            urgency_level = "LOW_MONITOR"
            
        scored_zones.append({
            "zone_id": z.id,
            "name": z.name,
            "priority_score": priority_score,
            "urgency_level": urgency_level,
            "factors": {
                "severity": z.severity,
                "population": z.population,
                "bayesian_risk": bayes_r,
                "total_critical_items": total_items_needed
            }
        })
        
    # Sort descending by priority_score
    scored_zones.sort(key=lambda x: x["priority_score"], reverse=True)
    
    rank_items = []
    for idx, item in enumerate(scored_zones, start=1):
        rank_items.append(PriorityRankingItem(
            zone_id=item["zone_id"],
            name=item["name"],
            rank=idx,
            priority_score=item["priority_score"],
            urgency_level=item["urgency_level"],
            factors=item["factors"]
        ))
        
    return rank_items
