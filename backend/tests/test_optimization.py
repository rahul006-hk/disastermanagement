from app.ai.optimization import ResourceOptimizationEngine
from app.schemas.schemas import ZoneBase, WarehouseBase, PriorityRankingItem

def test_ortools_optimization():
    engine = ResourceOptimizationEngine()
    zones = [
        ZoneBase(id="Z1", name="Zone 1", lat=13.0, lng=80.0, population=10000, severity="Critical", critical_needs={"food": 100, "water": 200})
    ]
    warehouses = [
        WarehouseBase(id="W1", name="Warehouse 1", lat=13.05, lng=80.05, stock={"food": 500, "water": 1000})
    ]
    priorities = [
        PriorityRankingItem(zone_id="Z1", name="Zone 1", rank=1, priority_score=85.0, urgency_level="CRITICAL_IMMEDIATE", factors={})
    ]
    
    result = engine.optimize_allocations(zones, warehouses, priorities)
    assert result.critical_coverage_percentage > 0.0
    assert len(result.allocations) >= 1
    assert result.allocations[0].resources_allocated["food"] == 100
