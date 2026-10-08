import React from "react";
import { Activity, Play, RefreshCw, ShieldCheck } from "lucide-react";

interface NavbarProps {
  onSimulate: () => void;
  onGeneratePlan: () => void;
  loading: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({ onSimulate, onGeneratePlan, loading }) => {
  return (
    <header className="bg-slate-900 border-b border-slate-800 text-white px-6 py-4 flex items-center justify-between shadow-xl">
      <div className="flex items-center space-x-3">
        <div className="bg-rose-600 p-2.5 rounded-xl shadow-lg shadow-rose-600/30">
          <Activity className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="font-bold text-xl tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
            Disaster Relief AI Planner
          </h1>
          <p className="text-xs text-slate-400 font-medium">
            Dynamic Emergency Resource Allocation Engine
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-3">
        <button
          onClick={onSimulate}
          disabled={loading}
          className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400 hover:bg-amber-500/20 text-sm font-semibold transition-all disabled:opacity-50"
        >
          <Play className="w-4 h-4" />
          <span>Simulate Disaster Event</span>
        </button>

        <button
          onClick={onGeneratePlan}
          disabled={loading}
          className="flex items-center space-x-2 px-5 py-2.5 rounded-lg bg-gradient-to-r from-rose-600 to-rose-700 hover:from-rose-500 hover:to-rose-600 text-white text-sm font-bold shadow-lg shadow-rose-600/20 transition-all disabled:opacity-50"
        >
          {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <ShieldCheck className="w-4 h-4" />}
          <span>Run AI Optimization Plan</span>
        </button>
      </div>
    </header>
  );
};
