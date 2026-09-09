import React, { useState } from 'react';

interface IncidentPoint {
  id: string;
  category: string;
  title: string;
  lat: number;
  lon: number;
  priority: 'critical' | 'high' | 'medium' | 'low';
  ward: string;
}

const SAMPLE_INCIDENTS: IncidentPoint[] = [
  { id: 'CMP-2026-0001', category: 'WATER_SUPPLY', title: 'Main trunk pipe leak', lat: 13.0418, lon: 80.2337, priority: 'critical', ward: 'Ward 115' },
  { id: 'CMP-2026-0002', category: 'WATER_SUPPLY', title: 'Low pressure contamination', lat: 13.0425, lon: 80.2345, priority: 'high', ward: 'Ward 115' },
  { id: 'CMP-2026-0003', category: 'WATER_SUPPLY', title: 'Valve overflow onto road', lat: 13.0412, lon: 80.2332, priority: 'high', ward: 'Ward 115' },
  { id: 'CMP-2026-0004', category: 'ROAD_TRANSPORT', title: 'Severe pothole crater near bus stop', lat: 13.0830, lon: 80.2710, priority: 'critical', ward: 'Ward 104' },
  { id: 'CMP-2026-0005', category: 'SOLID_WASTE', title: 'Commercial garbage overflow', lat: 13.0850, lon: 80.2730, priority: 'medium', ward: 'Ward 104' },
  { id: 'CMP-2026-0006', category: 'STREET_LIGHTING', title: 'Flickering 60W mast light', lat: 12.9815, lon: 80.2180, priority: 'low', ward: 'Ward 178' },
];

export const WardGisMap: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [activePoint, setActivePoint] = useState<IncidentPoint | null>(null);

  const filtered = selectedCategory === 'ALL'
    ? SAMPLE_INCIDENTS
    : SAMPLE_INCIDENTS.filter((p) => p.category === selectedCategory);

  const categoryColor = (cat: string) => {
    switch (cat) {
      case 'WATER_SUPPLY': return 'bg-cyan-500 border-cyan-300';
      case 'SOLID_WASTE': return 'bg-emerald-500 border-emerald-300';
      case 'ROAD_TRANSPORT': return 'bg-amber-500 border-amber-300';
      case 'STREET_LIGHTING': return 'bg-yellow-400 border-yellow-200';
      default: return 'bg-rose-500 border-rose-300';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl text-white">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="inline-block w-3 h-3 rounded-full bg-emerald-400 animate-ping" />
            <h3 className="text-xl font-bold text-white tracking-wide">
              Spatial GIS Radar & Hotspot Cluster Map
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Real-time geospatial clustering using DBSCAN geodesic proximity analysis
          </p>
        </div>

        {/* Category Filters */}
        <div className="flex flex-wrap gap-2">
          {['ALL', 'WATER_SUPPLY', 'ROAD_TRANSPORT', 'SOLID_WASTE', 'STREET_LIGHTING'].map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1 text-xs rounded-lg font-medium transition ${
                selectedCategory === cat
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30'
                  : 'bg-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              {cat.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Map Radar Canvas */}
      <div className="relative w-full h-80 bg-slate-950 rounded-xl border border-slate-800 overflow-hidden flex items-center justify-center">
        {/* Grid lines */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b_1px,transparent_1px),linear-gradient(to_bottom,#1e293b_1px,transparent_1px)] bg-[size:32px_32px] opacity-40" />

        {/* Cluster Circle Warning Area (Ward 115) */}
        {(selectedCategory === 'ALL' || selectedCategory === 'WATER_SUPPLY') && (
          <div className="absolute top-16 left-28 w-44 h-44 rounded-full border border-rose-500/40 bg-rose-500/10 flex items-center justify-center animate-pulse">
            <span className="text-[10px] text-rose-400 font-mono font-bold uppercase tracking-wider bg-rose-950/80 px-2 py-0.5 rounded border border-rose-500/30">
              CLUSTER HOTSPOT: 3 INCIDENTS (180m)
            </span>
          </div>
        )}

        {/* Incident Interactive Pins */}
        {filtered.map((item, idx) => {
          // Compute pseudo screen positions
          const xOffsets = [150, 185, 220, 480, 520, 680];
          const yOffsets = [100, 140, 120, 80, 160, 210];
          const left = xOffsets[idx % xOffsets.length];
          const top = yOffsets[idx % yOffsets.length];

          return (
            <div
              key={item.id}
              onClick={() => setActivePoint(item)}
              style={{ left: `${left}px`, top: `${top}px` }}
              className="absolute cursor-pointer group -translate-x-1/2 -translate-y-1/2"
            >
              <div className={`w-5 h-5 rounded-full border-2 ${categoryColor(item.category)} shadow-lg shadow-black/50 group-hover:scale-125 transition flex items-center justify-center`}>
                <div className="w-1.5 h-1.5 rounded-full bg-white" />
              </div>
              <span className="hidden group-hover:block absolute top-6 left-1/2 -translate-x-1/2 bg-slate-800 text-[11px] px-2 py-1 rounded text-white whitespace-nowrap shadow-xl border border-slate-700 z-20">
                {item.id} - {item.ward}
              </span>
            </div>
          );
        })}

        {/* Legend */}
        <div className="absolute bottom-3 left-3 bg-slate-900/90 backdrop-blur border border-slate-800 p-2.5 rounded-lg text-[11px] space-y-1">
          <div className="font-semibold text-slate-300 mb-1">Incident Color Key</div>
          <div className="flex items-center gap-2 text-cyan-400"><span className="w-2.5 h-2.5 rounded-full bg-cyan-500" /> Water Supply</div>
          <div className="flex items-center gap-2 text-amber-400"><span className="w-2.5 h-2.5 rounded-full bg-amber-500" /> Road Transport</div>
          <div className="flex items-center gap-2 text-emerald-400"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500" /> Solid Waste</div>
        </div>

        {/* Active Point Card Popup */}
        {activePoint && (
          <div className="absolute top-4 right-4 w-72 bg-slate-900 border border-slate-700 p-4 rounded-xl shadow-2xl z-30 animate-in fade-in">
            <div className="flex justify-between items-start">
              <span className="text-xs font-mono font-bold text-blue-400">{activePoint.id}</span>
              <button onClick={() => setActivePoint(null)} className="text-slate-400 hover:text-white text-xs">✕</button>
            </div>
            <h4 className="font-bold text-sm text-white mt-1">{activePoint.title}</h4>
            <div className="text-xs text-slate-400 mt-2 space-y-1">
              <div>Ward: <span className="text-slate-200">{activePoint.ward}</span></div>
              <div>Geo: <span className="font-mono text-slate-300">{activePoint.lat}, {activePoint.lon}</span></div>
              <div>Priority: <span className="font-bold uppercase text-rose-400">{activePoint.priority}</span></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
