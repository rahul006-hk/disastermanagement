import React from "react";
import type { DecisionExplanation } from "../types/api";
import { HelpCircle } from "lucide-react";

interface XaiProps {
  explanations: DecisionExplanation[];
}

export const XaiPanel: React.FC<XaiProps> = ({ explanations }) => {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 shadow-xl">
      <h3 className="text-lg font-bold text-white mb-4 flex items-center space-x-2">
        <HelpCircle className="w-5 h-5 text-amber-400" />
        <span>Explainable AI (XAI) Decision Rationale & Traces</span>
      </h3>
      <div className="space-y-4">
        {explanations.map((item, idx) => (
          <div key={idx} className="bg-slate-800/40 border border-slate-700/60 p-4 rounded-xl space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-xs font-bold px-2.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
                {item.decision_type}
              </span>
              <span className="text-xs text-slate-400 font-mono">Target: {item.target_id}</span>
            </div>
            <h4 className="font-bold text-white text-sm">{item.summary}</h4>
            <p className="text-xs text-slate-300"><span className="font-semibold text-amber-400">Rationale:</span> {item.rationale}</p>
            <p className="text-xs text-slate-400"><span className="font-semibold text-emerald-400">Expected Outcome:</span> {item.expected_outcome}</p>
            <div className="text-xs text-slate-500 flex items-center space-x-2 pt-1 border-t border-slate-700/50">
              <span>Constraints: {item.constraints_considered.join(" • ")}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
