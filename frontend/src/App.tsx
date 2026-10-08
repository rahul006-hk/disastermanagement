import React, { useEffect, useState } from "react";
import { api } from "./services/api";
import type {
  Zone, Warehouse, Hospital, Shelter, Road,
  ActionPlanResult, EvaluationMetrics
} from "./types/api";
import { Navbar } from "./components/Navbar";
import { DisasterMap } from "./components/DisasterMap";
import { SituationAssessmentCard } from "./components/SituationAssessmentCard";
import { PriorityTable } from "./components/PriorityTable";
import { ActionPlanView } from "./components/ActionPlanView";
import { XaiPanel } from "./components/XaiPanel";
import { WhatIfSimulator } from "./components/WhatIfSimulator";
import { EvaluationDashboard } from "./components/EvaluationDashboard";
import { Map, Table, ShieldCheck, HelpCircle, Sliders, Award } from "lucide-react";

export const App: React.FC = () => {
  const [zones, setZones] = useState<Zone[]>([]);
  const [warehouses, setWarehouses] = useState<Warehouse[]>([]);
  const [hospitals, setHospitals] = useState<Hospital[]>([]);
  const [shelters, setShelters] = useState<Shelter[]>([]);
  const [roads, setRoads] = useState<Road[]>([]);
  const [plan, setPlan] = useState<ActionPlanResult | null>(null);
  const [metrics, setMetrics] = useState<EvaluationMetrics[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"map" | "plan" | "priority" | "xai" | "whatif" | "eval">("map");

  const loadAllData = async () => {
    try {
      const [zData, wData, hData, sData, rData] = await Promise.all([
        api.getZones(),
        api.getWarehouses(),
        api.getHospitals(),
        api.getShelters(),
        api.getRoads(),
      ]);
      setZones(zData);
      setWarehouses(wData);
      setHospitals(hData);
      setShelters(sData);
      setRoads(rData);
    } catch (err) {
      console.error("Failed to load initial data", err);
    }
  };

  const handleGeneratePlan = async () => {
    setLoading(true);
    try {
      const planRes = await api.generateActionPlan();
      setPlan(planRes);
      const evalRes = await api.getEvaluationMetrics();
      setMetrics(evalRes);
      await loadAllData();
    } catch (err) {
      console.error("Plan generation error", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSimulate = async () => {
    setLoading(true);
    try {
      await api.simulateScenario(15);
      await loadAllData();
      await handleGeneratePlan();
    } catch (err) {
      console.error("Simulation error", err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleRoad = async (roadId: string, currentBlocked: boolean) => {
    try {
      await api.toggleRoadBlockage(roadId, !currentBlocked);
      await loadAllData();
      if (plan) {
        await handleGeneratePlan();
      }
    } catch (err) {
      console.error("Toggle road error", err);
    }
  };

  useEffect(() => {
    loadAllData();
    handleGeneratePlan();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar onSimulate={handleSimulate} onGeneratePlan={handleGeneratePlan} loading={loading} />

      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
        <SituationAssessmentCard assessment={plan?.assessment || null} />

        {/* Tab Navigation */}
        <div className="flex space-x-2 border-b border-slate-800 pb-2 text-sm font-semibold overflow-x-auto">
          <button
            onClick={() => setActiveTab("map")}
            className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg transition-all whitespace-nowrap ${
              activeTab === "map"
                ? "bg-rose-600 text-white shadow-lg shadow-rose-600/30 font-bold"
                : "text-slate-400 hover:bg-slate-900 hover:text-white"
            }`}
          >
            <Map className="w-4 h-4" />
            <span>Interactive Map & Routes</span>
          </button>

          <button
            onClick={() => setActiveTab("priority")}
            className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg transition-all whitespace-nowrap ${
              activeTab === "priority"
                ? "bg-rose-600 text-white shadow-lg shadow-rose-600/30 font-bold"
                : "text-slate-400 hover:bg-slate-900 hover:text-white"
            }`}
          >
            <Table className="w-4 h-4" />
            <span>Priority Ranking</span>
          </button>

          <button
            onClick={() => setActiveTab("plan")}
            className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg transition-all whitespace-nowrap ${
              activeTab === "plan"
                ? "bg-rose-600 text-white shadow-lg shadow-rose-600/30 font-bold"
                : "text-slate-400 hover:bg-slate-900 hover:text-white"
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            <span>Action Plan & Dispatch</span>
          </button>

          <button
            onClick={() => setActiveTab("xai")}
            className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg transition-all whitespace-nowrap ${
              activeTab === "xai"
                ? "bg-rose-600 text-white shadow-lg shadow-rose-600/30 font-bold"
                : "text-slate-400 hover:bg-slate-900 hover:text-white"
            }`}
          >
            <HelpCircle className="w-4 h-4" />
            <span>Explainable AI (XAI)</span>
          </button>

          <button
            onClick={() => setActiveTab("whatif")}
            className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg transition-all whitespace-nowrap ${
              activeTab === "whatif"
                ? "bg-rose-600 text-white shadow-lg shadow-rose-600/30 font-bold"
                : "text-slate-400 hover:bg-slate-900 hover:text-white"
            }`}
          >
            <Sliders className="w-4 h-4" />
            <span>What-If Simulator</span>
          </button>

          <button
            onClick={() => setActiveTab("eval")}
            className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg transition-all whitespace-nowrap ${
              activeTab === "eval"
                ? "bg-rose-600 text-white shadow-lg shadow-rose-600/30 font-bold"
                : "text-slate-400 hover:bg-slate-900 hover:text-white"
            }`}
          >
            <Award className="w-4 h-4" />
            <span>Evaluation Benchmarks</span>
          </button>
        </div>

        {/* Tab Contents */}
        {activeTab === "map" && (
          <DisasterMap
            zones={zones}
            warehouses={warehouses}
            hospitals={hospitals}
            shelters={shelters}
            roads={roads}
            routes={plan?.routes || []}
            onToggleRoad={handleToggleRoad}
          />
        )}

        {activeTab === "priority" && <PriorityTable priorities={plan?.priorities || []} />}

        {activeTab === "plan" && <ActionPlanView plan={plan} />}

        {activeTab === "xai" && <XaiPanel explanations={plan?.explanations || []} />}

        {activeTab === "whatif" && <WhatIfSimulator />}

        {activeTab === "eval" && <EvaluationDashboard metrics={metrics} />}
      </main>

      <footer className="bg-slate-900/60 border-t border-slate-800 text-center py-4 text-xs text-slate-500">
        Disaster Relief AI Resource Allocation Planner &bull; Deterministic MILP + A* + pgmpy Engine
      </footer>
    </div>
  );
};

export default App;
