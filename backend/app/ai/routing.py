import math
from typing import List, Dict, Tuple, Optional
import networkx as nx
from app.schemas.schemas import RouteResult, RouteStep, RoadBase, ZoneBase, WarehouseBase

class DynamicRoutingEngine:
    def __init__(self, roads: List[RoadBase], nodes_geo: Dict[str, Tuple[float, float]]):
        """
        Phase 10: A* Dynamic Routing Engine
        Builds a NetworkX weighted graph, handling blocked roads and calculating A* paths.
        """
        self.roads = roads
        self.nodes_geo = nodes_geo
        self.graph = nx.Graph()
        
        # Populate nodes & coordinates
        for node_id, (lat, lng) in nodes_geo.items():
            self.graph.add_node(node_id, lat=lat, lng=lng)
            
        # Add edges (Roads)
        for r in roads:
            # If blocked, set infinite / prohibitive weight for routing
            weight = float('inf') if r.is_blocked else r.travel_time_min
            self.graph.add_edge(
                r.source,
                r.target,
                id=r.id,
                distance_km=r.distance_km,
                travel_time_min=r.travel_time_min,
                weight=weight,
                is_blocked=r.is_blocked
            )

    def _heuristic_distance(self, u: str, v: str) -> float:
        """Euclidean distance heuristic for A* in coordinate space."""
        if u not in self.nodes_geo or v not in self.nodes_geo:
            return 0.0
        lat1, lng1 = self.nodes_geo[u]
        lat2, lng2 = self.nodes_geo[v]
        # Approximate distance in km
        dlat = (lat2 - lat1) * 111.0
        dlng = (lng2 - lng1) * 111.0 * math.cos(math.radians(lat1))
        return math.sqrt(dlat*dlat + dlng*dlng)

    def find_best_route(self, source: str, target: str) -> Optional[RouteResult]:
        """Runs NetworkX A* search between source and target."""
        try:
            path = nx.astar_path(
                self.graph,
                source,
                target,
                heuristic=self._heuristic_distance,
                weight="weight"
            )
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None
            
        total_dist = 0.0
        total_time = 0.0
        steps = []
        
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            edge_data = self.graph.get_edge_data(u, v)
            dist = edge_data.get("distance_km", 1.0)
            time = edge_data.get("travel_time_min", 5.0)
            blocked = edge_data.get("is_blocked", False)
            
            total_dist += dist
            total_time += time
            steps.append(RouteStep(
                from_node=u,
                to_node=v,
                distance_km=dist,
                time_min=time,
                is_blocked=blocked
            ))
            
        return RouteResult(
            source_warehouse=source,
            target_zone=target,
            path=path,
            total_distance_km=round(total_dist, 2),
            total_time_min=round(total_time, 2),
            steps=steps
        )
