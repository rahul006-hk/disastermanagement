# Disaster Relief AI Team Development Status

## Project Overview
Disaster Relief Resource Allocation Planner built with FastAPI, NetworkX, pgmpy, OR-Tools, SimPy, PostgreSQL, and React + Leaflet.

## Status Matrix
- [x] **Phase 1 — Git + Project Setup**: Environment, directory layout, configuration files.
- [x] **Phase 2 — Database + Models**: SQLAlchemy models, PostgreSQL connection, SQLite fallback, seed data, unit tests.
- [x] **Phase 3 — FastAPI Foundation**: REST endpoints for Scenarios, Zones, Roads, Resources, Vehicles, Hospitals, Shelters.
- [x] **Phase 4 — React Foundation**: Layout, TypeScript types, Leaflet map setup, API service layer.
- [x] **Phase 5 — Scenario Simulator**: SimPy event engine for flood & dynamic disaster propagation.
- [x] **Phase 6 — Interactive Map**: React Leaflet dashboard with blocked roads & entity markers.
- [x] **Phase 7 — Situation Assessment**: Severity index, affected population & critical needs scoring.
- [x] **Phase 8 — Bayesian Risk**: Config-driven pgmpy Bayesian Network (`bayesian_model.json`).
- [x] **Phase 9 — Priority Ranking**: Urgency ranking algorithm based on severity & Bayesian risk.
- [x] **Phase 10 — A* Routing**: NetworkX road graph with dynamic travel times & road blockages.
- [x] **Phase 11 — Resource Optimization**: Google OR-Tools MIP solver with configurable weights (`optimization_weights.json`).
- [x] **Phase 12 — Constraint Validation**: Multi-level constraint checker for vehicle capacity, stock, bed limits.
- [x] **Phase 13 — Automated Action Planning**: End-to-end pipeline generator producing executable dispatch plans.
- [x] **Phase 14 — Assignments**: Dedicated Vehicle, Hospital bed, and Shelter facility assignments.
- [x] **Phase 15 — Dynamic Replanning**: WebSocket live event stream & auto-replan on road/demand state changes.
- [x] **Phase 16 — Explainable AI (XAI)**: Decision trace generator explaining why routes & allocations were selected.
- [x] **Phase 17 — What-If Simulation & Evaluation**: Comparative engine benchmarking vs Random, Equal & Greedy baselines.

## Implemented Technical Suggestions
1. **Automated OpenAPI / TypeScript Contract Types**: `src/types/api.ts` mirrors backend Pydantic models.
2. **Standardized Coordinate Schemas**: Shared `(lat, lng)` floats for NetworkX nodes and Leaflet markers.
3. **Formalized Multi-Objective Configuration**: `config/optimization_weights.json` for OR-Tools MILP solver weights.
4. **Real-Time WebSockets Replanning**: FastAPI WebSocket router (`/ws/replanning`).
5. **Externalized Bayesian Network DAG**: `config/bayesian_model.json` loaded at runtime for pgmpy inference.

## Verification
- **Backend Tests**: 7/7 Pytest unit tests passed (`pytest backend/tests/`).
- **Frontend Build**: Vite + TypeScript build succeeded (`npm run build`).
