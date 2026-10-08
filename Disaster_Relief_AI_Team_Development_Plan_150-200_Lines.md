# Disaster Relief Resource Allocation Planner
## Team Development Plan
## 1. Scope
1. Scenario Simulator
2. Interactive Disaster Map
3. Situation & Severity Assessment
4. Bayesian Risk Prediction
5. Priority Ranking
6. A* Dynamic Routing
7. Resource Allocation Optimization
8. Constraint Validation
9. Automated Action Planning
10. Dynamic Replanning
11. Vehicle Assignment
12. Hospital Allocation
13. Shelter Allocation
14. Explainable AI
15. What-If Simulation
## 2. Tech Stack
- **Backend/AI:** Python, FastAPI, NetworkX, pgmpy, OR-Tools, SimPy, Pandas, NumPy
- **Frontend:** React, TypeScript, Tailwind CSS, React Leaflet, OpenStreetMap, Recharts
- **Database:** PostgreSQL; PostGIS only if actually required
- **Testing:** Pytest
- **Optional LLM:** natural-language input/explanations only; never the source of truth for routes, quantities, probabilities, capacities or optimization.
## 3. Architecture
```text
React → FastAPI → AI/Planning Engine → PostgreSQL
                     ├─ Bayesian Risk
                     ├─ Priority Ranking
                     ├─ A* Routing
                     ├─ OR-Tools Optimization
                     ├─ Constraint Validation
                     └─ Automated Planning
SimPy → Scenario/Event Simulation
```
Main flow:
```text
Scenario → Assessment → Risk → Priority → Route + Optimize
→ Validate → Action Plan → New Event → Replan
```
## 4. Initial Data
- 8 affected zones, 2 warehouses, 4 hospitals, 4 shelters
- 12 vehicles, 8 rescue teams
- Resources: food, water, medicine, medical supplies, shelter kits
- Vehicles: ambulance, relief truck, rescue vehicle
- Hospitals: capacity, beds, emergency capability, location, incoming patients
- Shelters: capacity, occupancy, location, facilities, accessibility
- All values must be configurable. **Do not invent unapproved values.**
## 5. Repository
```text
disaster-relief-ai/
├── backend/app/{api,models,schemas,services,ai,simulation}
├── backend/tests/
├── frontend/src/{components,pages,maps,services,types,hooks}
├── data/ docs/ scripts/
├── .env.example
├── docker-compose.yml
└── README.md
```
# 6. EXACT BUILD ORDER
### Phase 1 — Git + Project Setup
1. Create repository and `main`.
2. Create backend/frontend structure.
3. Add `.gitignore`, `.env.example`, README.
4. Set up Python, React and PostgreSQL Docker.
5. Confirm every teammate can clone and run.
### Phase 2 — Database + Models
1. Connect PostgreSQL.
2. Create: Disaster, Scenario, Zone, Road, Warehouse, Resource, Vehicle, Team, Hospital, Shelter, Event, Plan.
3. Add seed data and read/write tests.
### Phase 3 — FastAPI Foundation
1. Create FastAPI app + DB connection + health check.
2. Add schemas/services.
3. Add:
```text
GET/POST /api/scenarios
GET /api/zones
GET /api/roads
GET /api/resources
GET /api/vehicles
GET /api/hospitals
GET /api/shelters
```
### Phase 4 — React Foundation
1. Create React + TypeScript app.
2. Configure Tailwind, layout and routing.
3. Create API service layer and shared types.
4. Connect dashboard to FastAPI.
### Phase 5 — Scenario Simulator
1. Generate flood scenario, affected zones and demand.
2. Generate road damage/blockages.
3. Generate resource, hospital and shelter states.
4. Store scenario and add simulation controls.
### Phase 6 — Interactive Map
1. Add React Leaflet + OpenStreetMap.
2. Display zones, roads, warehouses, hospitals, shelters, vehicles and teams.
3. Display blocked roads and connect to scenario API.
### Phase 7 — Situation Assessment
Calculate severity, affected population, critical needs and infrastructure status.
Return a structured `SituationAssessment`.
### Phase 8 — Bayesian Risk
1. Define approved Bayesian variables/probabilities.
2. Build pgmpy model.
3. Input scenario observations and return risk probabilities.
4. Add fixed test scenarios.
**Rule:** probabilities must be approved/configured, never invented.
### Phase 9 — Priority Ranking
Use assessment + risk to rank zones by urgency. Return ordered zones and ranking factors.
### Phase 10 — A* Routing
1. Build NetworkX road graph with distance/time.
2. Mark blocked roads.
3. Run A* and return route, distance and ETA.
4. Test blocked-road cases.
### Phase 11 — Resource Optimization
Use OR-Tools with supply, demand, priority, vehicle limits and constraints.
Output allocation + unmet demand.
Objectives:
- Primary: maximize critical-needs coverage and population served.
- Secondary: minimize response time, distance, wastage and unmet demand.
**Do not invent objective weights.**
### Phase 12 — Constraint Validation
Validate resource availability, vehicle capacity, hospital/shelter capacity, team availability, route availability and delivery limits.
Return:
```text
valid
violations[]
warnings[]
```
### Phase 13 — Automated Action Planning
Combine priority, routes, optimization, constraints and available vehicles/teams.
Generate an ordered action plan using actual engine outputs only.
### Phase 14 — Assignments
- **Vehicles:** ambulance → medical; relief truck → supplies; rescue vehicle → rescue teams.
- **Hospitals:** beds, capability, route and incoming patients.
- **Shelters:** capacity, accessibility, location and facilities.
All assignments must pass constraints.
### Phase 15 — Dynamic Replanning
Trigger when a road, resource, hospital, shelter or demand changes.
```text
New Event → Update State → Risk → Priority → Routes
→ Optimization → Constraints → New Action Plan
```
### Phase 16 — Explainable AI
For every major decision show: decision, important inputs, constraints, reason and expected result.
### Phase 17 — What-If Simulation
Let users change road status, resource quantity, population, hospital/shelter capacity or disaster severity. Re-run and compare.
# 7. GIT / TEAM WORKFLOW
Never push unfinished work directly to `main`.
```text
main
├── feature/database
├── feature/scenario
├── feature/bayesian
├── feature/routing
├── feature/optimization
├── feature/planning
└── feature/frontend
```
Workflow:
```text
pull main → create branch → implement → test → commit → push
→ Pull Request → review → merge → pull latest main
```
Every merged feature must include working code, tests, clear interface/API and no hidden assumptions.
# 8. HANDOFF RULE
A feature is **handoff-ready** only when:
```text
Code works + Tests pass + Interface documented
+ Assumptions documented + Changes merged to main
```
Before continuing another teammate's work:
```text
git pull → run tests → run app → verify feature → continue
```
Keep `docs/STATUS.md`:
```text
DONE
IN PROGRESS
BLOCKED
NEXT
```
# 9. AI CODING ASSISTANT RULES
- Never hallucinate requirements or data.
- Never invent probabilities, capacities, quantities or results.
- Never silently choose important architecture decisions.
- If information is missing, ask the team.
- Mark values: `Confirmed`, `Configured`, `Simulated`, `AI-Inferred`, or `Unknown`.
- Never claim implementation until tested.
- Never claim performance improvement until measured.
- Major architecture changes require team approval.
- LLM is not the planning decision source of truth.
# 10. EVALUATION
Compare:
1. Random allocation
2. Equal allocation
3. Greedy priority allocation
4. Proposed AI planner
Measure: population served, critical demand satisfaction, response time, travel distance, resource utilization/wastage, unmet demand, constraint violations, emergency assignment success and replanning effectiveness.
**Never fabricate results.**
# 11. FINAL INTEGRATION
```text
Database → FastAPI → Simulator → Map → Assessment → Bayesian Risk
→ Priority → A* → Optimization → Constraints → Planning
→ Vehicle/Hospital/Shelter Assignment → Replanning
→ Explainability → What-If → Testing
```
**Final target:** create scenario → analyze risk → prioritize zones → find routes → allocate resources → assign facilities → validate → explain → simulate changes → replan.
## Project Status
Use `docs/STATUS.md` so any teammate can pull `main` and immediately know what is done, in progress, blocked and next.
