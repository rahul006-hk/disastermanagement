import React, { useState } from "react";
import { api } from "../services/api";
import { Sliders, RefreshCw, ArrowRight } from "lucide-react";

export const WhatIfSimulator: React.FC = () => {
  const [targetRoad, setTargetRoad] = useState("R5");
  const [roadBlocked, setRoadBlocked] = useState(true);
  const [zoneSeverity, setZoneSeverity] = useState("Critical");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleRunWhatIf = async () => {
    setLoading(true);
    try {
      const payload = {
        road_blockages: { [targetRoad]: roadBlocked },
        zone_severity_override: { Z3: zoneSeverity },
        resource_delta: { W1: { food: -1000 } }
      };
      const res = await api.runWhatIf(payload);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 shadow-xl space-y-4">
      <h3 className="text-lg font-bold text-white flex items-center space-x-2">
        <Sliders className="w-5 h-5 text-indigo-400" />
        <span>What-If Scenario Simulation Modifier</span>
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div>
          <label className="block text-slate-400 mb-1">Target Road Damage</label>
          <div className="flex space-x-2">
            <select
              value={targetRoad}
              onChange={(e) => setTargetRoad(e.target.value)}
              className="bg-slate-800 text-white rounded p-2 border border-slate-700 flex-1"
            >
              <option value="R1">R1 (W1 -&gt; Z1)</option>
              <option value="R2">R2 (W1 -&gt; Z3)</option>
              <option value="R5">R5 (W2 -&gt; Z6)</option>
              <option value="R8">R8 (Z3 -&gt; Z4)</option>
            </select>
            <button
              onClick={() => setRoadBlocked(!roadBlocked)}
              className={`px-3 py-1 rounded font-bold ${
                roadBlocked ? "bg-rose-500/20 text-rose-400 border border-rose-500/30" : "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
              }`}
            >
              {roadBlocked ? "Blocked" : "Open"}
            </button>
          </div>
        </div>

        <div>
          <label className="block text-slate-400 mb-1">Zone 3 Severity Override</label>
          <select
            value={zoneSeverity}
            onChange={(e) => setZoneSeverity(e.target.value)}
            className="bg-slate-800 text-white rounded p-2 border border-slate-700 w-full"
          >
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </div>

        <div className="flex items-end">
          <button
            onClick={handleRunWhatIf}
            disabled={loading}
            className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg shadow-lg shadow-indigo-600/20 flex justify-center items-center space-x-2 disabled:opacity-50"
          >
            {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <ArrowRight className="w-4 h-4" />}
            <span>Run What-If Comparison</span>
          </button>
        </div>
      </div>

      {result && (
        <div className="bg-slate-800/40 border border-slate-700/60 p-4 rounded-xl space-y-2 text-xs text-slate-300">
          <h4 className="font-bold text-white text-sm">What-If Delta Comparison Result</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            <div className="p-2 bg-slate-800 rounded"><span className="text-slate-400">Coverage Shift:</span> <p className="font-bold text-emerald-400">{result.diff_summary.coverage_change_percent}%</p></div>
            <div className="p-2 bg-slate-800 rounded"><span className="text-slate-400">Served Pop Delta:</span> <p className="font-bold text-white">{result.diff_summary.population_served_delta}</p></div>
            <div className="p-2 bg-slate-800 rounded"><span className="text-slate-400">New Violations:</span> <p className="font-bold text-rose-400">{result.diff_summary.new_violations_introduced}</p></div>
            <div className="p-2 bg-slate-800 rounded"><span className="text-slate-400">Routes Shifted:</span> <p className="font-bold text-blue-400">{result.diff_summary.route_changes_count}</p></div>
          </div>
        </div>
      )}
    </div>
  );
};
