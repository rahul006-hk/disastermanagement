# Disaster Relief Resource Allocation Planner

An AI-driven emergency response decision support platform combining **FastAPI**, **NetworkX A* Routing**, **pgmpy Bayesian Risk Modeling**, **Google OR-Tools MIP Optimization**, **SimPy Discrete Event Simulation**, **PostgreSQL**, and **React + Leaflet**.

## Key System Modules
1. **Scenario Simulator (SimPy)**: Simulates dynamic disaster propagation, road blockages, and supply shifts.
2. **Interactive Disaster Map (React + Leaflet)**: Real-time spatial tracking of 8 zones, 2 warehouses, 4 hospitals, 4 shelters, vehicles, and blocked roads.
3. **Situation Assessment**: Computes urgency index based on affected population and infrastructure damage.
4. **Bayesian Risk Engine (pgmpy)**: Probabilistic risk assessment based on external environmental factors.
5. **Priority Ranking**: Multi-attribute ranking algorithm for affected zones.
6. **A* Dynamic Routing (NetworkX)**: Real-time route optimization taking road damage & blockages into account.
7. **Resource Allocation (OR-Tools)**: Mixed Integer Linear Programming (MILP) solver optimizing resource distribution.
8. **Constraint Validator**: Enforces vehicle capacity, hospital bed, shelter occupancy, and stock limits.
9. **Automated Action Planner**: Generates ordered, actionable dispatch plans.
10. **Dynamic Replanning**: Real-time event detection via WebSockets and automatic plan updates.
11. **Explainable AI (XAI)**: Full decision trace and rationale for routing and resource allocation choices.
12. **What-If Simulation & Evaluation**: Comparative benchmarks against Random, Equal, and Greedy baselines.

## Quick Start

### Backend
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r backend/requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Running Tests
```bash
pytest backend/tests/
```
