from app.ai.routing import DynamicRoutingEngine
from app.schemas.schemas import RoadBase

def test_routing_engine():
    roads = [
        RoadBase(id="R1", source="W1", target="Z1", distance_km=5.0, travel_time_min=10.0, is_blocked=False),
        RoadBase(id="R2", source="Z1", target="Z2", distance_km=3.0, travel_time_min=5.0, is_blocked=True),
        RoadBase(id="R3", source="W1", target="Z2", distance_km=12.0, travel_time_min=20.0, is_blocked=False)
    ]
    nodes_geo = {"W1": (13.0, 80.0), "Z1": (13.1, 80.1), "Z2": (13.2, 80.2)}
    
    router = DynamicRoutingEngine(roads, nodes_geo)
    
    # Path W1 -> Z2 should avoid blocked R2 (Z1->Z2) and use direct R3 (W1->Z2)
    route = router.find_best_route("W1", "Z2")
    assert route is not None
    assert route.path == ["W1", "Z2"]
    assert route.total_distance_km == 12.0
