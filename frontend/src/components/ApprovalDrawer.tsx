import React, { useState } from 'react';
import { X, CheckCircle, AlertTriangle, ShieldCheck, ArrowRight, CornerDownRight } from 'lucide-react';
import { ComplaintRecord } from '../types';
import { PolicyCitationPanel } from './PolicyCitationPanel';
import { api } from '../services/api';

interface ApprovalDrawerProps {
  complaint: ComplaintRecord;
  isOpen: boolean;
  onClose: () => void;
  onApproved: (updated: ComplaintRecord) => void;
  lang: 'en' | 'ta';
  t: any;
}

export const ApprovalDrawer: React.FC<ApprovalDrawerProps> = ({
  complaint,
  isOpen,
  onClose,
  onApproved,
  lang,
  t
}) => {
  const rec = complaint.recommendation;
  const [isOverride, setIsOverride] = useState(false);
  const [overrideDept, setOverrideDept] = useState(rec?.suggested_department || 'Water Supply & Sewerage Board');
  const [overridePriority, setOverridePriority] = useState(rec?.priority_score || 'MEDIUM');
  const [overrideReason, setOverrideReason] = useState('');
  const [officerNotes, setOfficerNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen || !rec) return null;

  const handleConfirm = async () => {
    setSubmitting(true);
    try {
      const updated = await api.approveRouting(complaint.id, {
        approved_department: isOverride ? overrideDept : rec.suggested_department,
        approved_priority: isOverride ? overridePriority : rec.priority_score,
        override_reason: isOverride ? overrideReason : undefined,
        officer_notes: officerNotes || undefined
      });
      onApproved(updated);
      onClose();
    } catch (err: any) {
      alert(`Approval error: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-slate-900/50 backdrop-blur-sm flex justify-end">
      <div className="w-full max-w-xl bg-white shadow-2xl h-full flex flex-col overflow-y-auto">
        {/* Drawer Header */}
        <div className="p-5 border-b border-slate-200 bg-slate-900 text-white flex items-center justify-between sticky top-0 z-10">
          <div className="flex items-center space-x-2.5">
            <ShieldCheck className="w-5 h-5 text-sky-400" />
            <div>
              <h3 className="text-base font-bold">{t.drawer.title}</h3>
              <p className="text-xs text-slate-400">Case ID: {complaint.id.slice(0, 13)}...</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Drawer Body */}
        <div className="p-6 space-y-6 flex-1">
          {/* Grievance Summary Box */}
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block mb-1">
              {lang === 'ta' ? 'புகார் விவரம் (மறைக்கப்பட்டது)' : 'Citizen Grievance (Redacted)'}
            </span>
            <p className="text-xs text-slate-800 font-medium">{complaint.redacted_content}</p>
            <div className="flex items-center space-x-3 mt-2 text-[11px] text-slate-500">
              <span>{complaint.ward}</span>
              <span>&bull;</span>
              <span>{complaint.zone}</span>
            </div>
          </div>

          {/* AI Recommendation Card */}
          <div className="p-4 rounded-xl border-2 border-sky-500/30 bg-sky-50/40 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-sky-900 uppercase tracking-wider">
                {t.drawer.aiRecommendation}
              </span>
              <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-sky-100 text-sky-800">
                {(rec.confidence * 100).toFixed(0)}% Confidence
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-2.5 bg-white rounded-lg border border-slate-200">
                <span className="text-[10px] text-slate-500 block">{t.drawer.suggestedDept}</span>
                <span className="font-bold text-slate-900">{rec.suggested_department}</span>
              </div>
              <div className="p-2.5 bg-white rounded-lg border border-slate-200">
                <span className="text-[10px] text-slate-500 block">{t.drawer.suggestedPriority}</span>
                <span className={`font-bold px-2 py-0.5 rounded text-[11px] inline-block mt-0.5 ${
                  rec.priority_score === 'CRITICAL' ? 'bg-rose-100 text-rose-800' :
                  rec.priority_score === 'HIGH' ? 'bg-amber-100 text-amber-800' :
                  'bg-emerald-100 text-emerald-800'
                }`}>
                  {rec.priority_score}
                </span>
              </div>
            </div>

            {/* Reasons List */}
            <div className="space-y-1 text-xs text-slate-700">
              {rec.reasons.map((r, i) => (
                <p key={i} className="flex items-start space-x-1.5">
                  <CornerDownRight className="w-3.5 h-3.5 text-sky-600 flex-shrink-0 mt-0.5" />
                  <span>{r}</span>
                </p>
              ))}
            </div>
          </div>

          {/* Missing Evidence Warning */}
          {rec.missing_evidence && rec.missing_evidence.length > 0 && (
            <div className="p-3.5 bg-amber-50 rounded-xl border border-amber-200 text-xs text-amber-900 space-y-1">
              <span className="font-bold flex items-center space-x-1">
                <AlertTriangle className="w-4 h-4 text-amber-600" />
                <span>{t.drawer.missingEvidence}</span>
              </span>
              <ul className="list-disc list-inside space-y-0.5 pl-1">
                {rec.missing_evidence.map((me, i) => (
                  <li key={i}>{me}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Grounded Policy Citations */}
          <PolicyCitationPanel citations={rec.citations} lang={lang} t={t} />

          {/* Override Toggle Form */}
          <div className="pt-2 border-t border-slate-200 space-y-3">
            <label className="flex items-center space-x-2 text-xs font-semibold text-slate-800 cursor-pointer">
              <input
                type="checkbox"
                checked={isOverride}
                onChange={(e) => setIsOverride(e.target.checked)}
                className="w-4 h-4 rounded text-sky-600 focus:ring-sky-500"
              />
              <span>{t.drawer.overrideToggle}</span>
            </label>

            {isOverride && (
              <div className="space-y-3 p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs">
                <div>
                  <label className="font-medium text-slate-700 block mb-1">{t.drawer.overrideDept}</label>
                  <select
                    value={overrideDept}
                    onChange={(e) => setOverrideDept(e.target.value)}
                    className="w-full p-2 rounded-lg border border-slate-300 text-xs focus:ring-sky-500"
                  >
                    <option value="Water Supply & Sewerage Board">Water Supply & Sewerage Board</option>
                    <option value="Solid Waste Management">Solid Waste Management</option>
                    <option value="Roads & Bridges">Roads & Bridges</option>
                    <option value="Electrical & Street Lighting">Electrical & Street Lighting</option>
                    <option value="Public Health & Sanitation">Public Health & Sanitation</option>
                  </select>
                </div>

                <div>
                  <label className="font-medium text-slate-700 block mb-1">{t.drawer.overridePriority}</label>
                  <select
                    value={overridePriority}
                    onChange={(e) => setOverridePriority(e.target.value as any)}
                    className="w-full p-2 rounded-lg border border-slate-300 text-xs focus:ring-sky-500"
                  >
                    <option value="CRITICAL">CRITICAL</option>
                    <option value="HIGH">HIGH</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="LOW">LOW</option>
                  </select>
                </div>

                <div>
                  <label className="font-medium text-slate-700 block mb-1">{t.drawer.overrideReason} *</label>
                  <input
                    type="text"
                    required
                    value={overrideReason}
                    onChange={(e) => setOverrideReason(e.target.value)}
                    placeholder="e.g. Field inspection reveals water contamination originated from road culvert project"
                    className="w-full p-2 rounded-lg border border-slate-300 text-xs"
                  />
                </div>
              </div>
            )}

            {/* Officer Notes */}
            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">
                {lang === 'ta' ? 'துறைக்கான வழிகாட்டல் குறிப்புகள்' : 'Internal Dispatch Instructions'}
              </label>
              <textarea
                rows={2}
                value={officerNotes}
                onChange={(e) => setOfficerNotes(e.target.value)}
                placeholder="e.g. Inspect water valve at junction; collect water quality sample for lab testing."
                className="w-full rounded-lg border border-slate-300 p-2.5 text-xs focus:ring-sky-500"
              />
            </div>
          </div>
        </div>

        {/* Drawer Footer */}
        <div className="p-4 border-t border-slate-200 bg-slate-50 sticky bottom-0 z-10">
          <button
            id="confirm-routing-btn"
            onClick={handleConfirm}
            disabled={submitting || (isOverride && !overrideReason.trim())}
            className="w-full py-3 px-4 bg-sky-600 hover:bg-sky-700 text-white text-xs font-bold rounded-xl shadow transition disabled:opacity-50 flex items-center justify-center space-x-2"
          >
            <CheckCircle className="w-4 h-4" />
            <span>{submitting ? 'Processing...' : t.drawer.confirmBtn}</span>
          </button>
        </div>
      </div>
    </div>
  );
};
