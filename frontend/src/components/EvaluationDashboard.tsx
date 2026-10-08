import React from "react";
import type { EvaluationMetrics } from "../types/api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { Award } from "lucide-react";

interface EvaluationProps {
  metrics: EvaluationMetrics[];
}

export const EvaluationDashboard: React.FC<EvaluationProps> = ({ metrics }) => {
  if (!metrics || metrics.length === 0) return null;

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 shadow-xl space-y-4">
      <h3 className="text-lg font-bold text-white flex items-center space-x-2">
        <Award className="w-5 h-5 text-emerald-400" />
        <span>Algorithm Benchmark Evaluation vs Baselines (Section 10)</span>
      </h3>

      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={metrics} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <XAxis dataKey="planner_name" stroke="#94a3b8" fontSize={11} />
            <YAxis stroke="#94a3b8" fontSize={11} />
            <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", color: "#fff" }} />
            <Legend />
            <Bar dataKey="critical_demand_coverage_percent" name="Coverage %" fill="#10b981" radius={[4, 4, 0, 0]} />
            <Bar dataKey="avg_response_time_min" name="Avg Time (min)" fill="#f59e0b" radius={[4, 4, 0, 0]} />
            <Bar dataKey="assignment_success_rate_percent" name="Success Rate %" fill="#3b82f6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        {metrics.map((m, idx) => (
          <div key={idx} className={`p-3 rounded-lg border text-xs space-y-1 ${m.planner_name.includes("Proposed") ? "bg-emerald-500/10 border-emerald-500/40 text-white" : "bg-slate-800/40 border-slate-700/50 text-slate-300"}`}>
            <h4 className="font-bold">{m.planner_name}</h4>
            <p>Coverage: <span className="font-bold text-emerald-400">{m.critical_demand_coverage_percent}%</span></p>
            <p>Avg Time: <span className="font-bold text-amber-400">{m.avg_response_time_min} mins</span></p>
            <p>Violations: <span className="font-bold text-rose-400">{m.constraint_violations}</span></p>
          </div>
        ))}
      </div>
    </div>
  );
};
