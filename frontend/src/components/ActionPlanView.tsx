import React from "react";
import type { ActionPlanResult } from "../types/api";
import { Truck, Hospital, Home, AlertTriangle, CheckCircle } from "lucide-react";

interface ActionPlanProps {
  plan: ActionPlanResult | null;
}

export const ActionPlanView: React.FC<ActionPlanProps> = ({ plan }) => {
  if (!plan) return null;

  const { optimization, validation, assignments } = plan;

  return (
    <div className="space-y-6">
      {/* Optimization & Validation Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-xl">
          <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-2">OR-Tools Solver Output</h3>
          <div className="space-y-2 text-sm text-white">
            <p className="flex justify-between"><span>Critical Need Coverage:</span> <span className="font-bold text-emerald-400">{optimization.critical_coverage_percentage}%</span></p>
            <p className="flex justify-between"><span>Total Citizens Served:</span> <span className="font-bold">{optimization.total_population_served.toLocaleString()}</span></p>
            <p className="flex justify-between"><span>Objective Score:</span> <span className="font-mono text-blue-400">{optimization.objective_value}</span></p>
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-xl">
          <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-2">Constraint Validator</h3>
          <div className="flex items-center space-x-2 mb-2">
            {validation.valid ? (
              <span className="flex items-center space-x-1 text-emerald-400 font-bold text-sm bg-emerald-500/10 px-2.5 py-1 rounded-md">
                <CheckCircle className="w-4 h-4" /> <span>PASSED ALL CONSTRAINTS</span>
              </span>
            ) : (
              <span className="flex items-center space-x-1 text-rose-400 font-bold text-sm bg-rose-500/10 px-2.5 py-1 rounded-md">
                <AlertTriangle className="w-4 h-4" /> <span>VIOLATIONS DETECTED</span>
              </span>
            )}
          </div>
          {validation.warnings.length > 0 && (
            <p className="text-xs text-amber-400 mt-1">Warnings: {validation.warnings.join("; ")}</p>
          )}
        </div>
      </div>

      {/* Vehicle Dispatch Assignments */}
      <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-xl">
        <h3 className="text-base font-bold text-white mb-3 flex items-center space-x-2">
          <Truck className="w-5 h-5 text-blue-400" />
          <span>Vehicle Dispatch Assignments ({assignments.vehicles.length} Units)</span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {assignments.vehicles.map((v, idx) => (
            <div key={idx} className="bg-slate-800/40 border border-slate-700/50 p-3 rounded-lg text-xs space-y-1">
              <div className="flex justify-between font-bold text-white">
                <span>{v.vehicle_name} ({v.type})</span>
                <span className="text-emerald-400">{v.status}</span>
              </div>
              <p className="text-slate-400">Origin: <span className="text-white">{v.origin_warehouse}</span> &rarr; Target: <span className="text-white">{v.target_zone}</span></p>
              <p className="text-slate-400">Payload: {JSON.stringify(v.payload)}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Hospital & Shelter Assignments */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-xl">
          <h3 className="text-base font-bold text-white mb-3 flex items-center space-x-2">
            <Hospital className="w-5 h-5 text-rose-400" />
            <span>Hospital Bed & Patient Allocations</span>
          </h3>
          <div className="space-y-2">
            {assignments.hospitals.map((h, idx) => (
              <div key={idx} className="bg-slate-800/40 p-2.5 rounded-lg text-xs flex justify-between items-center text-slate-300">
                <div>
                  <p className="font-bold text-white">{h.source_zone_name} &rarr; {h.hospital_name}</p>
                  <p className="text-slate-400">Transferred: {h.patients_transferred} patients via Ambulance {h.assigned_ambulance}</p>
                </div>
                <span className="text-emerald-400 font-bold">{h.hospital_remaining_beds} beds left</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-xl">
          <h3 className="text-base font-bold text-white mb-3 flex items-center space-x-2">
            <Home className="w-5 h-5 text-emerald-400" />
            <span>Shelter Evacuation Allocations</span>
          </h3>
          <div className="space-y-2">
            {assignments.shelters.map((s, idx) => (
              <div key={idx} className="bg-slate-800/40 p-2.5 rounded-lg text-xs flex justify-between items-center text-slate-300">
                <div>
                  <p className="font-bold text-white">{s.source_zone_name} &rarr; {s.shelter_name}</p>
                  <p className="text-slate-400">Evacuees: {s.evacuees_assigned} citizens ({s.accessibility} access)</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
