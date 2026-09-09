import React, { useState, useEffect } from 'react';
import { Activity, BellRing, Clock, UserCheck, Zap, AlertCircle } from 'lucide-react';

interface LiveEvent {
  id: string;
  time: string;
  category: string;
  ward: string;
  priority: 'critical' | 'high' | 'medium';
  action: string;
}

export const LiveCockpitRadar: React.FC = () => {
  const [events, setEvents] = useState<LiveEvent[]>([
    { id: 'CMP-2026-0007', time: '10s ago', category: 'WATER_SUPPLY', ward: 'Ward 115', priority: 'critical', action: 'Ultrasonic sensor triggered main line leak' },
    { id: 'CMP-2026-0008', time: '45s ago', category: 'ROAD_TRANSPORT', ward: 'Ward 104', priority: 'high', action: 'Citizen filed Tamil voice note for asphalt pothole' },
    { id: 'CMP-2026-0009', time: '2m ago', category: 'STREET_LIGHTING', ward: 'Ward 178', priority: 'medium', action: 'Photocell lux sensor failure detected' },
  ]);

  const [activeOfficersCount] = useState<number>(8);
  const [claimedCases, setClaimedCases] = useState<Set<string>>(new Set());

  const handleClaim = (id: string) => {
    setClaimedCases((prev) => new Set(prev).add(id));
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl text-white">
      {/* Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6 border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <div className="relative">
            <span className="w-3 h-3 rounded-full bg-rose-500 inline-block animate-ping" />
            <span className="w-3 h-3 rounded-full bg-rose-600 inline-block absolute top-0 left-0" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              Live Municipal Cockpit & Incident Radar
              <span className="text-[11px] font-mono font-semibold bg-rose-500/20 text-rose-400 border border-rose-500/30 px-2 py-0.5 rounded-full">
                WS ACTIVE
              </span>
            </h3>
            <p className="text-xs text-slate-400">Continuous WebSocket feed from Ward Incident Desks</p>
          </div>
        </div>

        {/* Telemetry Chips */}
        <div className="flex items-center gap-3 text-xs">
          <div className="bg-slate-950 border border-slate-800 px-3 py-1.5 rounded-lg flex items-center gap-2">
            <UserCheck className="w-4 h-4 text-cyan-400" />
            <span><strong className="text-cyan-300">{activeOfficersCount}</strong> Officers On-Duty</span>
          </div>
          <div className="bg-slate-950 border border-slate-800 px-3 py-1.5 rounded-lg flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            <span>Triage Latency: <strong className="text-emerald-300">&lt;180ms</strong></span>
          </div>
        </div>
      </div>

      {/* Live Event Stream Table */}
      <div className="space-y-2.5">
        {events.map((evt) => {
          const isClaimed = claimedCases.has(evt.id);
          return (
            <div
              key={evt.id}
              className={`p-3.5 rounded-xl border transition flex flex-col md:flex-row md:items-center justify-between gap-3 ${
                isClaimed
                  ? 'bg-slate-950/40 border-slate-800/60 opacity-60'
                  : evt.priority === 'critical'
                  ? 'bg-rose-950/20 border-rose-500/30'
                  : 'bg-slate-950 border-slate-800'
              }`}
            >
              <div className="flex items-start gap-3">
                <div className={`p-2 rounded-lg mt-0.5 ${
                  evt.priority === 'critical' ? 'bg-rose-500/20 text-rose-400' : 'bg-blue-500/20 text-blue-400'
                }`}>
                  {evt.priority === 'critical' ? <AlertCircle className="w-4 h-4" /> : <Clock className="w-4 h-4" />}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold text-white">{evt.id}</span>
                    <span className="text-[10px] font-semibold bg-slate-800 text-slate-300 px-2 py-0.5 rounded">
                      {evt.ward}
                    </span>
                    <span className={`text-[10px] font-bold uppercase px-1.5 py-0.5 rounded ${
                      evt.priority === 'critical' ? 'bg-rose-500 text-white' : 'bg-amber-500/20 text-amber-300'
                    }`}>
                      {evt.priority}
                    </span>
                    <span className="text-[11px] text-slate-500 font-mono">{evt.time}</span>
                  </div>
                  <p className="text-xs text-slate-300 mt-1">{evt.action}</p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-2 self-end md:self-auto">
                {isClaimed ? (
                  <span className="text-xs text-emerald-400 font-semibold flex items-center gap-1">
                    <UserCheck className="w-4 h-4" /> Claimed by You
                  </span>
                ) : (
                  <button
                    onClick={() => handleClaim(evt.id)}
                    className="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold transition flex items-center gap-1.5 shadow-md shadow-blue-500/20"
                  >
                    <Zap className="w-3.5 h-3.5" /> Claim Case
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
