import simpy
import random
from typing import List, Dict, Any
from app.schemas.schemas import ZoneBase, RoadBase

class DisasterScenarioSimulator:
    def __init__(self, zones: List[ZoneBase], roads: List[RoadBase]):
        """
        Phase 5: Scenario Simulator powered by SimPy.
        Discrete-event simulation engine for disaster propagation, road blockages, and demand spikes.
        """
        self.env = simpy.Environment()
        self.zones = zones
        self.roads = roads
        self.events_log: List[Dict[str, Any]] = []

    def _flood_propagation_process(self):
        """Simulates flood water level rising every 5 simulation ticks."""
        while True:
            yield self.env.timeout(5)
            # Randomly affect a zone
            target_zone = random.choice(self.zones)
            if target_zone.severity != "Critical":
                target_zone.severity = "Critical" if target_zone.severity == "High" else "High"
                event_entry = {
                    "tick": self.env.now,
                    "event_type": "DEMAND_SPIKE",
                    "target_id": target_zone.id,
                    "description": f"Flood level surge in {target_zone.name}! Severity upgraded to {target_zone.severity}."
                }
                self.events_log.append(event_entry)

    def _road_collapse_process(self):
        """Simulates landslides / road debris blocking roads every 8 ticks."""
        while True:
            yield self.env.timeout(8)
            unblocked_roads = [r for r in self.roads if not r.is_blocked]
            if unblocked_roads:
                blocked_road = random.choice(unblocked_roads)
                blocked_road.is_blocked = True
                event_entry = {
                    "tick": self.env.now,
                    "event_type": "ROAD_BLOCKAGE",
                    "target_id": blocked_road.id,
                    "description": f"Landslide on road {blocked_road.source}->{blocked_road.target}! Road is now BLOCKED."
                }
                self.events_log.append(event_entry)

    def run_simulation(self, total_ticks: int = 20) -> List[Dict[str, Any]]:
        """Runs the SimPy simulation up to specified duration ticks."""
        self.env.process(self._flood_propagation_process())
        self.env.process(self._road_collapse_process())
        self.env.run(until=total_ticks)
        return self.events_log
