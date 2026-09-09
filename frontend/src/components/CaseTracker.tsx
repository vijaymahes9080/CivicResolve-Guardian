import React, { useState, useEffect } from 'react';
import { Search, CheckCircle2, Clock, AlertCircle, ShieldCheck, ArrowRight } from 'lucide-react';
import { ComplaintRecord } from '../types';
import { api } from '../services/api';

interface CaseTrackerProps {
  initialCaseId?: string;
  lang: 'en' | 'ta';
  t: any;
}

export const CaseTracker: React.FC<CaseTrackerProps> = ({ initialCaseId, lang, t }) => {
  const [searchId, setSearchId] = useState(initialCaseId || '');
  const [complaint, setComplaint] = useState<ComplaintRecord | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (idToSearch?: string) => {
    const id = idToSearch || searchId;
    if (!id.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const data = await api.getComplaint(id.trim());
      setComplaint(data);
    } catch (err: any) {
      setError(err.message || 'Complaint not found');
      setComplaint(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (initialCaseId) {
      handleSearch(initialCaseId);
    }
  }, [initialCaseId]);

  const steps = [
    { key: 'SUBMITTED', label: lang === 'ta' ? 'பதிவு செய்யப்பட்டது' : 'Submitted' },
    { key: 'TRIAGED_PENDING_APPROVAL', label: lang === 'ta' ? 'AI பரிசீலனையில்' : 'Triaged' },
    { key: 'ROUTED_ASSIGNED', label: lang === 'ta' ? 'துறைக்கு அனுப்பப்பட்டது' : 'Routed' },
    { key: 'IN_PROGRESS', label: lang === 'ta' ? 'நடவடிக்கையில் உள்ளது' : 'In Progress' },
    { key: 'VERIFIED_RESOLVED', label: lang === 'ta' ? 'தீர்க்கப்பட்டது' : 'Verified Resolved' },
  ];

  const getStepIndex = (status: string) => {
    const map: Record<string, number> = {
      SUBMITTED: 0,
      TRIAGED_PENDING_APPROVAL: 1,
      ROUTED_ASSIGNED: 2,
      IN_PROGRESS: 3,
      ACTION_PROPOSED: 3,
      RESOLVED_PENDING_VERIFICATION: 3,
      VERIFIED_RESOLVED: 4
    };
    return map[status] ?? 0;
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      {/* Search Header */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 space-y-4">
        <h2 className="text-xl font-bold text-slate-900">{t.tracker.title}</h2>
        <div className="flex gap-2">
          <input
            id="tracker-search-input"
            type="text"
            value={searchId}
            onChange={(e) => setSearchId(e.target.value)}
            placeholder={t.tracker.searchPlaceholder}
            className="flex-1 rounded-xl border border-slate-300 px-4 py-2.5 text-xs text-slate-800 focus:ring-2 focus:ring-sky-500"
          />
          <button
            id="tracker-search-btn"
            onClick={() => handleSearch()}
            disabled={loading}
            className="px-5 py-2.5 bg-sky-600 hover:bg-sky-700 text-white rounded-xl text-xs font-semibold shadow-sm transition disabled:opacity-50"
          >
            {loading ? 'Searching...' : 'Track'}
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800 flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {complaint && (
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sm:p-8 space-y-8">
          {/* Progress Steps Timeline */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              {t.tracker.timeline}
            </h3>
            <div className="flex items-center justify-between relative">
              <div className="absolute top-1/2 left-0 right-0 h-1 bg-slate-200 -translate-y-1/2 z-0" />
              {steps.map((s, idx) => {
                const currentIdx = getStepIndex(complaint.status);
                const isPassed = idx <= currentIdx;
                const isCurrent = idx === currentIdx;

                return (
                  <div key={s.key} className="relative z-10 flex flex-col items-center">
                    <div
                      className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition ${
                        isCurrent
                          ? 'bg-sky-600 text-white ring-4 ring-sky-100'
                          : isPassed
                          ? 'bg-emerald-600 text-white'
                          : 'bg-slate-200 text-slate-500'
                      }`}
                    >
                      {isPassed && !isCurrent ? <CheckCircle2 className="w-4 h-4" /> : idx + 1}
                    </div>
                    <span className="text-[11px] font-semibold text-slate-700 mt-2 text-center max-w-[80px]">
                      {s.label}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Key Metric Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
            <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-500 text-[10px] block">{t.tracker.status}</span>
              <span className="font-bold text-slate-900 mt-0.5 block">{complaint.status.replace(/_/g, ' ')}</span>
            </div>
            <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-500 text-[10px] block">{t.tracker.department}</span>
              <span className="font-bold text-slate-900 mt-0.5 block">{complaint.department || 'Awaiting Triage'}</span>
            </div>
            <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-500 text-[10px] block">{t.tracker.priority}</span>
              <span className="font-bold text-slate-900 mt-0.5 block">{complaint.priority}</span>
            </div>
            <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-500 text-[10px] block">{t.tracker.slaDue}</span>
              <span className="font-bold text-sky-800 mt-0.5 block flex items-center">
                <Clock className="w-3.5 h-3.5 mr-1 text-sky-600" />
                48 Hours Target
              </span>
            </div>
          </div>

          {/* Grievance Note */}
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block">
              {lang === 'ta' ? 'பதிவு செய்யப்பட்ட புகார்' : 'Your Submitted Grievance'}
            </span>
            <p className="text-xs text-slate-800 leading-relaxed font-medium">{complaint.redacted_content}</p>
          </div>

          {/* Resolution Result if Verified */}
          {complaint.status === 'VERIFIED_RESOLVED' && (
            <div className="p-5 bg-emerald-50 rounded-2xl border border-emerald-200 space-y-2">
              <div className="flex items-center space-x-2 text-emerald-800">
                <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                <h4 className="text-sm font-bold">Grievance Verified & Resolved</h4>
              </div>
              <p className="text-xs text-emerald-900 font-medium">
                {complaint.resolution_summary || 'Remediation completed by municipal field engineering crew.'}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
