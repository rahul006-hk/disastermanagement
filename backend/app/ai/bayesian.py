import json
import os
from typing import List, Dict
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from app.schemas.schemas import BayesianRiskResult, ZoneBase

class BayesianRiskEngine:
    def __init__(self, config_path: str = None):
        if not config_path:
            config_path = os.path.join(os.path.dirname(__file__), "..", "config", "bayesian_model.json")
        
        with open(config_path, "r") as f:
            self.config = json.load(f)
            
        self.model = DiscreteBayesianNetwork(self.config["edges"])
        
        # Build CPDs from config
        cpts_config = self.config["cpts"]
        cpds = []
        for node, data in cpts_config.items():
            evidence = data.get("evidence")
            evidence_card = data.get("evidence_card")
            
            # Include state_names for target variable and all evidence variables
            state_names = {node: data["states"]}
            if evidence:
                for ev_node in evidence:
                    state_names[ev_node] = cpts_config[ev_node]["states"]

            cpd = TabularCPD(
                variable=node,
                variable_card=len(data["states"]),
                values=data["values"],
                evidence=evidence,
                evidence_card=evidence_card,
                state_names=state_names
            )
            cpds.append(cpd)
            
        self.model.add_cpds(*cpds)
        assert self.model.check_model(), "Invalid Bayesian Network CPD Configuration"
        self.infer = VariableElimination(self.model)

    def evaluate_zone_risks(self, zones: List[ZoneBase], rainfall_evidence: str = "Medium") -> BayesianRiskResult:
        """
        Phase 8: Bayesian Risk Inference
        Evaluates secondary disaster risk probabilities for affected zones using pgmpy.
        """
        zone_risks = {}
        risk_factors = {}
        
        # Inference for overall scenario condition
        query_sec = self.infer.query(
            variables=["SecondaryDisasterRisk"],
            evidence={"RainfallSeverity": rainfall_evidence}
        )
        query_road = self.infer.query(
            variables=["RoadBlockageRisk"],
            evidence={"RainfallSeverity": rainfall_evidence}
        )
        
        # High secondary disaster probability
        sec_high_prob = float(query_sec.values[1])
        road_block_prob = float(query_road.values[1])
        
        sev_multiplier = {"Critical": 1.3, "High": 1.1, "Medium": 0.9, "Low": 0.7}
        
        for z in zones:
            mult = sev_multiplier.get(z.severity, 1.0)
            calculated_risk = round(min(0.99, max(0.05, sec_high_prob * mult)), 3)
            zone_risks[z.id] = calculated_risk
            risk_factors[z.id] = {
                "rainfall_factor": rainfall_evidence,
                "road_blockage_probability": round(road_block_prob, 3),
                "secondary_disaster_probability": calculated_risk
            }
            
        return BayesianRiskResult(
            zone_risks=zone_risks,
            risk_factors=risk_factors,
            evidence_used={"RainfallSeverity": rainfall_evidence}
        )
