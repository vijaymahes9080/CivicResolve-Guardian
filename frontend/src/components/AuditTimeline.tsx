import React, { useState, useEffect } from 'react';
import { ShieldCheck, Key, Clock, User, AlertCircle } from 'lucide-react';
import { AuditEvent } from '../types';
import { api } from '../services/api';

interface AuditTimelineProps {
  caseId: string;
  lang: 'en' | 'ta';
}

export const AuditTimeline: React.FC<AuditTimelineProps> = ({ caseId, lang }) => {
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!caseId) return;
    setLoading(true);
    api.getAuditTrail(caseId)
      .then((data) => setEvents(data))
      .catch((err) => console.error('Failed to load audit events', err))
      .finally(() => setLoading(false));
  }, [caseId]);

  if (loading) {
    return <div className="p-4 text-xs text-slate-500 text-center">Loading audit log...</div>;
  }

  if (events.length === 0) {
    return <div className="p-4 text-xs text-slate-500 text-center">No audit events recorded yet.</div>;
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between pb-2 border-b border-slate-200">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center space-x-1.5">
          <ShieldCheck className="w-4 h-4 text-sky-600" />
          <span>{lang === 'ta' ? 'பாதுகாக்கப்பட்ட தணிக்கை வரலாறு' : 'Cryptographic Audit Trail'}</span>
        </h4>
        <span className="text-[10px] font-mono text-slate-500">HMAC-SHA256 Signed</span>
      </div>

      <div className="relative pl-6 space-y-4 before:content-[''] before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-200">
        {events.map((ev) => (
          <div key={ev.id} className="relative group">
            {/* Timeline Dot */}
            <div className="absolute -left-6 top-1 w-2.5 h-2.5 rounded-full bg-sky-600 ring-4 ring-white" />

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200/80 text-xs space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-bold text-slate-900">{ev.action_type}</span>
                <span className="text-[10px] text-slate-500 flex items-center">
                  <Clock className="w-3 h-3 mr-1" />
                  {new Date(ev.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                </span>
              </div>

              <div className="flex items-center space-x-2 text-[11px] text-slate-600">
                <span className="capitalize px-1.5 py-0.2 bg-slate-200/70 rounded text-[10px] font-semibold">
                  {ev.actor_role}
                </span>
                {ev.previous_state && ev.new_state && (
                  <span>
                    {ev.previous_state} &rarr; <strong>{ev.new_state}</strong>
                  </span>
                )}
              </div>

              {/* Checksum Signature */}
              <div className="pt-1 flex items-center space-x-1 text-[10px] font-mono text-slate-400 truncate">
                <Key className="w-3 h-3 flex-shrink-0 text-slate-400" />
                <span className="truncate">Sig: {ev.signature}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
