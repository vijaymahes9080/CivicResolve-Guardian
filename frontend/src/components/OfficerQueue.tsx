import React, { useState, useEffect } from 'react';
import { Filter, Sparkles, CheckCircle2, Clock, ShieldCheck, AlertCircle, FileText, ChevronRight } from 'lucide-react';
import { ComplaintRecord } from '../types';
import { api } from '../services/api';

interface OfficerQueueProps {
  onSelectCase: (complaint: ComplaintRecord) => void;
  onOpenApproval: (complaint: ComplaintRecord) => void;
  onOpenResolution: (complaint: ComplaintRecord) => void;
  lang: 'en' | 'ta';
  t: any;
}

export const OfficerQueue: React.FC<OfficerQueueProps> = ({
  onSelectCase,
  onOpenApproval,
  onOpenResolution,
  lang,
  t
}) => {
  const [complaints, setComplaints] = useState<ComplaintRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedDept, setSelectedDept] = useState('');
  const [selectedPriority, setSelectedPriority] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [triagingId, setTriagingId] = useState<string | null>(null);

  const fetchQueue = async () => {
    setLoading(true);
    try {
      const data = await api.getComplaints({
        department: selectedDept || undefined,
        status: selectedStatus || undefined
      });
      setComplaints(data);
    } catch (err: any) {
      console.error('Failed to fetch queue', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQueue();
  }, [selectedDept, selectedStatus]);

  const handleRunTriage = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setTriagingId(id);
    try {
      await api.runTriage(id);
      await fetchQueue();
    } catch (err: any) {
      alert(`Triage error: ${err.message}`);
    } finally {
      setTriagingId(null);
    }
  };

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'CRITICAL':
        return 'bg-rose-100 text-rose-800 border-rose-200';
      case 'HIGH':
        return 'bg-amber-100 text-amber-800 border-amber-200';
      case 'MEDIUM':
        return 'bg-sky-100 text-sky-800 border-sky-200';
      default:
        return 'bg-slate-100 text-slate-800 border-slate-200';
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'VERIFIED_RESOLVED':
        return 'bg-emerald-100 text-emerald-800 border-emerald-300';
      case 'ROUTED_ASSIGNED':
        return 'bg-indigo-100 text-indigo-800 border-indigo-200';
      case 'TRIAGED_PENDING_APPROVAL':
        return 'bg-amber-100 text-amber-900 border-amber-300 animate-pulse';
      case 'RESOLVED_PENDING_VERIFICATION':
        return 'bg-purple-100 text-purple-900 border-purple-300';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">{t.officer.queueTitle}</h2>
          <p className="text-xs text-slate-500">{t.officer.queueSubtitle}</p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={fetchQueue}
            className="px-4 py-2 bg-white border border-slate-200 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-50 shadow-sm transition"
          >
            {lang === 'ta' ? 'புதுப்பிக்க' : 'Refresh Queue'}
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="p-4 bg-white rounded-xl shadow-sm border border-slate-200 grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
        <div>
          <label className="text-[11px] font-semibold text-slate-500 block mb-1">{t.officer.filterDept}</label>
          <select
            value={selectedDept}
            onChange={(e) => setSelectedDept(e.target.value)}
            className="w-full p-2 rounded-lg border border-slate-300 bg-slate-50 focus:ring-sky-500"
          >
            <option value="">All Departments</option>
            <option value="Water Supply & Sewerage Board">Water Supply & Sewerage Board</option>
            <option value="Solid Waste Management">Solid Waste Management</option>
            <option value="Roads & Bridges">Roads & Bridges</option>
            <option value="Electrical & Street Lighting">Electrical & Street Lighting</option>
            <option value="Public Health & Sanitation">Public Health & Sanitation</option>
          </select>
        </div>

        <div>
          <label className="text-[11px] font-semibold text-slate-500 block mb-1">{t.officer.filterPriority}</label>
          <select
            value={selectedPriority}
            onChange={(e) => setSelectedPriority(e.target.value)}
            className="w-full p-2 rounded-lg border border-slate-300 bg-slate-50 focus:ring-sky-500"
          >
            <option value="">All Priorities</option>
            <option value="CRITICAL">CRITICAL</option>
            <option value="HIGH">HIGH</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="LOW">LOW</option>
          </select>
        </div>

        <div>
          <label className="text-[11px] font-semibold text-slate-500 block mb-1">{t.officer.filterStatus}</label>
          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="w-full p-2 rounded-lg border border-slate-300 bg-slate-50 focus:ring-sky-500"
          >
            <option value="">All Statuses</option>
            <option value="SUBMITTED">SUBMITTED</option>
            <option value="TRIAGED_PENDING_APPROVAL">TRIAGED_PENDING_APPROVAL</option>
            <option value="ROUTED_ASSIGNED">ROUTED_ASSIGNED</option>
            <option value="IN_PROGRESS">IN_PROGRESS</option>
            <option value="RESOLVED_PENDING_VERIFICATION">RESOLVED_PENDING_VERIFICATION</option>
            <option value="VERIFIED_RESOLVED">VERIFIED_RESOLVED</option>
          </select>
        </div>
      </div>

      {/* Queue Table */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-xs text-slate-500">Loading grievances...</div>
        ) : complaints.length === 0 ? (
          <div className="p-12 text-center text-xs text-slate-500">No complaints matching filter criteria.</div>
        ) : (
          <div className="divide-y divide-slate-100">
            {complaints.map((c) => (
              <div
                key={c.id}
                onClick={() => onSelectCase(c)}
                className="p-4 sm:p-5 hover:bg-slate-50/80 transition cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-4"
              >
                <div className="space-y-1.5 flex-1 pr-4">
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-xs font-bold text-sky-800 bg-sky-50 px-2 py-0.5 rounded border border-sky-200">
                      #{c.id.slice(0, 8)}
                    </span>
                    <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full border ${getPriorityBadge(c.priority)}`}>
                      {c.priority}
                    </span>
                    <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${getStatusBadge(c.status)}`}>
                      {c.status.replace(/_/g, ' ')}
                    </span>
                    <span className="text-[11px] text-slate-500 font-medium">
                      {c.ward || 'Ward 12'} &bull; {c.zone || 'Zone 4'}
                    </span>
                  </div>

                  <p className="text-xs text-slate-800 line-clamp-2 font-medium">
                    {c.redacted_content}
                  </p>

                  <div className="flex items-center space-x-4 text-[11px] text-slate-500">
                    <span>Dept: <strong>{c.department || 'Not Assigned'}</strong></span>
                    {c.recommendation && (
                      <span className="text-indigo-600 font-semibold flex items-center">
                        <Sparkles className="w-3 h-3 mr-1" />
                        AI: {c.recommendation.suggested_department} ({(c.recommendation.confidence * 100).toFixed(0)}%)
                      </span>
                    )}
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center space-x-2 flex-shrink-0" onClick={(e) => e.stopPropagation()}>
                  {c.status === 'SUBMITTED' && (
                    <button
                      id={`triage-btn-${c.id.slice(0, 8)}`}
                      onClick={(e) => handleRunTriage(c.id, e)}
                      disabled={triagingId === c.id}
                      className="px-3 py-1.5 bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-700 hover:to-indigo-700 text-white rounded-lg text-xs font-semibold shadow-sm transition disabled:opacity-50 flex items-center space-x-1"
                    >
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>{triagingId === c.id ? 'Triaging...' : t.officer.runTriage}</span>
                    </button>
                  )}

                  {c.status === 'TRIAGED_PENDING_APPROVAL' && (
                    <button
                      id={`approve-btn-${c.id.slice(0, 8)}`}
                      onClick={() => onOpenApproval(c)}
                      className="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-xs font-semibold shadow-sm transition flex items-center space-x-1"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>{t.officer.approveRouting}</span>
                    </button>
                  )}

                  {(c.status === 'ROUTED_ASSIGNED' || c.status === 'IN_PROGRESS' || c.status === 'RESOLVED_PENDING_VERIFICATION') && (
                    <button
                      id={`verify-btn-${c.id.slice(0, 8)}`}
                      onClick={() => onOpenResolution(c)}
                      className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-semibold shadow-sm transition flex items-center space-x-1"
                    >
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>{t.officer.checkResolution}</span>
                    </button>
                  )}

                  <button
                    onClick={() => onSelectCase(c)}
                    className="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition"
                    title="View case detail"
                  >
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
