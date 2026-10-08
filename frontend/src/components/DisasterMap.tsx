import React from "react";
import { MapContainer, TileLayer, Popup, Polyline, CircleMarker } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import type { Zone, Warehouse, Hospital, Shelter, Road, RouteResult } from "../types/api";

// Fix standard Leaflet icon paths
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

interface DisasterMapProps {
  zones: Zone[];
  warehouses: Warehouse[];
  hospitals: Hospital[];
  shelters: Shelter[];
  roads: Road[];
  routes: RouteResult[];
  onToggleRoad: (roadId: string, currentBlockedState: boolean) => void;
}

export const DisasterMap: React.FC<DisasterMapProps> = ({
  zones,
  warehouses,
  hospitals,
  shelters,
  roads,
  routes,
  onToggleRoad,
}) => {
  const centerLat = 13.0650;
  const centerLng = 80.2500;

  // Build node lookup map for coordinates
  const nodeGeo: Record<string, [number, number]> = {};
  zones.forEach((z) => (nodeGeo[z.id] = [z.lat, z.lng]));
  warehouses.forEach((w) => (nodeGeo[w.id] = [w.lat, w.lng]));
  hospitals.forEach((h) => (nodeGeo[h.id] = [h.lat, h.lng]));
  shelters.forEach((s) => (nodeGeo[s.id] = [s.lat, s.lng]));

  const getSeverityColor = (sev: string) => {
    switch (sev) {
      case "Critical": return "#ef4444";
      case "High": return "#f97316";
      case "Medium": return "#eab308";
      default: return "#10b981";
    }
  };

  return (
    <div className="w-full h-[520px] rounded-2xl overflow-hidden border border-slate-800 shadow-2xl relative">
      <MapContainer
        center={[centerLat, centerLng]}
        zoom={12}
        scrollWheelZoom={true}
        className="w-full h-full z-0"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Roads Polyline rendering */}
        {roads.map((road) => {
          const p1 = nodeGeo[road.source];
          const p2 = nodeGeo[road.target];
          if (!p1 || !p2) return null;

          return (
            <Polyline
              key={road.id}
              positions={[p1, p2]}
              pathOptions={{
                color: road.is_blocked ? "#ef4444" : "#64748b",
                dashArray: road.is_blocked ? "6, 6" : undefined,
                weight: road.is_blocked ? 4 : 2,
                opacity: 0.8,
              }}
              eventHandlers={{
                click: () => onToggleRoad(road.id, road.is_blocked),
              }}
            />
          );
        })}

        {/* Active Calculated A* Routes */}
        {routes.map((r, idx) => {
          const points: [number, number][] = r.path
            .map((nodeId) => nodeGeo[nodeId])
            .filter((p): p is [number, number] => p !== undefined);

          if (points.length < 2) return null;

          return (
            <Polyline
              key={`route-${idx}`}
              positions={points}
              pathOptions={{
                color: "#3b82f6",
                weight: 5,
                opacity: 0.9,
              }}
            />
          );
        })}

        {/* Zones (Circle Markers with severity radius & color) */}
        {zones.map((z) => (
          <CircleMarker
            key={z.id}
            center={[z.lat, z.lng]}
            radius={16}
            pathOptions={{
              color: getSeverityColor(z.severity),
              fillColor: getSeverityColor(z.severity),
              fillOpacity: 0.6,
              weight: 3,
            }}
          >
            <Popup>
              <div className="text-slate-900 font-sans p-1">
                <h3 className="font-bold text-base">{z.name} ({z.id})</h3>
                <p className="text-xs font-semibold text-rose-600 uppercase">Severity: {z.severity}</p>
                <p className="text-xs">Population: {z.population.toLocaleString()}</p>
                <div className="mt-2 text-xs border-t pt-1">
                  <span className="font-bold">Critical Needs:</span>
                  <ul className="list-disc pl-4 mt-1">
                    {Object.entries(z.critical_needs).map(([k, v]) => (
                      <li key={k}>{k}: {v} units</li>
                    ))}
                  </ul>
                </div>
              </div>
            </Popup>
          </CircleMarker>
        ))}

        {/* Warehouses */}
        {warehouses.map((w) => (
          <CircleMarker
            key={w.id}
            center={[w.lat, w.lng]}
            radius={14}
            pathOptions={{
              color: "#2563eb",
              fillColor: "#3b82f6",
              fillOpacity: 0.85,
              weight: 2,
            }}
          >
            <Popup>
              <div className="p-1">
                <h3 className="font-bold text-sm text-blue-700">Depot {w.name}</h3>
                <p className="text-xs font-semibold">Stock Available:</p>
                <ul className="text-xs list-disc pl-4">
                  {Object.entries(w.stock).map(([k, v]) => (
                    <li key={k}>{k}: {v}</li>
                  ))}
                </ul>
              </div>
            </Popup>
          </CircleMarker>
        ))}

        {/* Hospitals */}
        {hospitals.map((h) => (
          <CircleMarker
            key={h.id}
            center={[h.lat, h.lng]}
            radius={12}
            pathOptions={{
              color: "#dc2626",
              fillColor: "#f87171",
              fillOpacity: 0.9,
              weight: 2,
            }}
          >
            <Popup>
              <div className="p-1">
                <h3 className="font-bold text-sm text-red-600">Hospital {h.name}</h3>
                <p className="text-xs">Beds Available: {h.available_beds} / {h.capacity}</p>
                <p className="text-xs">Emergency Capable: {h.emergency_capability ? "Yes" : "No"}</p>
              </div>
            </Popup>
          </CircleMarker>
        ))}

        {/* Shelters */}
        {shelters.map((s) => (
          <CircleMarker
            key={s.id}
            center={[s.lat, s.lng]}
            radius={12}
            pathOptions={{
              color: "#16a34a",
              fillColor: "#4ade80",
              fillOpacity: 0.9,
              weight: 2,
            }}
          >
            <Popup>
              <div className="p-1">
                <h3 className="font-bold text-sm text-emerald-600">Shelter {s.name}</h3>
                <p className="text-xs">Occupancy: {s.occupancy} / {s.capacity}</p>
                <p className="text-xs">Facilities: {s.facilities.join(", ")}</p>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>

      <div className="absolute bottom-4 left-4 bg-slate-900/90 backdrop-blur-md p-3 rounded-xl border border-slate-700 text-xs text-white z-10 flex space-x-4">
        <div className="flex items-center space-x-1.5">
          <span className="w-3 h-3 rounded-full bg-red-500 inline-block"></span>
          <span>Critical Zone</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-3 h-3 rounded-full bg-blue-500 inline-block"></span>
          <span>Depot Warehouse</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-3 h-3 rounded-full bg-rose-500 inline-block"></span>
          <span>Hospital</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span>
          <span>Shelter</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-4 h-0.5 border-t-2 border-dashed border-red-500 inline-block"></span>
          <span>Blocked Road (Click to toggle)</span>
        </div>
      </div>
    </div>
  );
};
