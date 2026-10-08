import React from "react";
import type { SituationAssessment } from "../types/api";
import { AlertCircle, Users, Package, ShieldAlert } from "lucide-react";

interface AssessmentProps {
  assessment: SituationAssessment | null;
}

export const SituationAssessmentCard: React.FC<AssessmentProps> = ({ assessment }) => {
  if (!assessment) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl flex items-center space-x-3">
        <div className="p-3 bg-rose-500/10 text-rose-500 rounded-lg">
          <AlertCircle className="w-6 h-6" />
        </div>
        <div>
          <p className="text-xs text-slate-400 font-medium uppercase">Severity Index</p>
          <p className="text-2xl font-bold text-white">{assessment.overall_severity_index} / 1.0</p>
        </div>
      </div>

      <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl flex items-center space-x-3">
        <div className="p-3 bg-blue-500/10 text-blue-500 rounded-lg">
          <Users className="w-6 h-6" />
        </div>
        <div>
          <p className="text-xs text-slate-400 font-medium uppercase">Total Affected Pop.</p>
          <p className="text-2xl font-bold text-white">{assessment.affected_population_total.toLocaleString()}</p>
        </div>
      </div>

      <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl flex items-center space-x-3">
        <div className="p-3 bg-amber-500/10 text-amber-500 rounded-lg">
          <Package className="w-6 h-6" />
        </div>
        <div>
          <p className="text-xs text-slate-400 font-medium uppercase">High Urgency Zones</p>
          <p className="text-2xl font-bold text-white">{assessment.high_urgency_zone_ids.length} Zones</p>
        </div>
      </div>

      <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl flex items-center space-x-3">
        <div className="p-3 bg-emerald-500/10 text-emerald-500 rounded-lg">
          <ShieldAlert className="w-6 h-6" />
        </div>
        <div>
          <p className="text-xs text-slate-400 font-medium uppercase">Infra Risk Score</p>
          <p className="text-2xl font-bold text-white">{assessment.infrastructure_risk_score * 100}%</p>
        </div>
      </div>
    </div>
  );
};
