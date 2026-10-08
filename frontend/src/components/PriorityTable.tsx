import React from "react";
import type { PriorityRankingItem } from "../types/api";

interface PriorityTableProps {
  priorities: PriorityRankingItem[];
}

export const PriorityTable: React.FC<PriorityTableProps> = ({ priorities }) => {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 shadow-xl">
      <h3 className="text-lg font-bold text-white mb-4 flex items-center space-x-2">
        <span>Zone Priority Ranking (Multi-Attribute + Bayesian Risk)</span>
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-300">
          <thead className="bg-slate-800/60 text-slate-400 uppercase text-xs">
            <tr>
              <th className="px-4 py-3">Rank</th>
              <th className="px-4 py-3">Zone</th>
              <th className="px-4 py-3">Score</th>
              <th className="px-4 py-3">Urgency Status</th>
              <th className="px-4 py-3">Severity</th>
              <th className="px-4 py-3">Bayesian Risk</th>
              <th className="px-4 py-3">Population</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {priorities.map((item) => (
              <tr key={item.zone_id} className="hover:bg-slate-800/40">
                <td className="px-4 py-3 font-bold text-white">#{item.rank}</td>
                <td className="px-4 py-3 font-semibold text-white">{item.name}</td>
                <td className="px-4 py-3 font-mono font-bold text-rose-400">{item.priority_score}</td>
                <td className="px-4 py-3">
                  <span
                    className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                      item.urgency_level === "CRITICAL_IMMEDIATE"
                        ? "bg-rose-500/20 text-rose-400 border border-rose-500/30"
                        : item.urgency_level === "HIGH_PRIORITY"
                        ? "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                        : "bg-slate-700/50 text-slate-300"
                    }`}
                  >
                    {item.urgency_level}
                  </span>
                </td>
                <td className="px-4 py-3">{item.factors.severity}</td>
                <td className="px-4 py-3 font-mono">{(item.factors.bayesian_risk * 100).toFixed(1)}%</td>
                <td className="px-4 py-3">{item.factors.population.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
