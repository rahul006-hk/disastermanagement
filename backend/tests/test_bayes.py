from app.ai.bayesian import BayesianRiskEngine
from app.schemas.schemas import ZoneBase

def test_bayesian_risk_engine():
    engine = BayesianRiskEngine()
    test_zones = [
        ZoneBase(id="Z1", name="Zone 1", lat=13.0, lng=80.0, population=10000, severity="Critical", critical_needs={"water": 500}),
        ZoneBase(id="Z2", name="Zone 2", lat=13.1, lng=80.1, population=5000, severity="Low", critical_needs={"food": 200})
    ]
    res = engine.evaluate_zone_risks(test_zones, rainfall_evidence="High")
    assert "Z1" in res.zone_risks
    assert "Z2" in res.zone_risks
    assert res.zone_risks["Z1"] > res.zone_risks["Z2"]
