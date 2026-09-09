import React, { useState } from 'react';
import { ArrowLeft, ShieldCheck, Lock, Unlock, FileText, CheckCircle2, AlertTriangle, Sparkles } from 'lucide-react';
import { ComplaintRecord } from '../types';
import { PolicyCitationPanel } from './PolicyCitationPanel';
import { AuditTimeline } from './AuditTimeline';

interface CaseDetailProps {
  complaint: ComplaintRecord;
  onBack: () => void;
  onOpenApproval: (c: ComplaintRecord) => void;
  onOpenResolution: (c: ComplaintRecord) => void;
  lang: 'en' | 'ta';
  t: any;
  role: 'citizen' | 'officer' | 'admin';
}

export const CaseDetail: React.FC<CaseDetailProps> = ({
  complaint,
  onBack,
  onOpenApproval,
  onOpenResolution,
  lang,
  t,
  role
}) => {
  const [showRaw, setShowRaw] = useState(false);
  const rec = complaint.recommendation;

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      {/* Back Button */}
      <button
        onClick={onBack}
        className="flex items-center space-x-1.5 text-xs font-semibold text-sky-700 hover:text-sky-900 transition"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>{lang === 'ta' ? 'பட்டியலுக்கு திரும்பு' : 'Back to Queue'}</span>
      </button>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Grievance & AI Triage */}
        <div className="lg:col-span-2 space-y-6">
          {/* Card: Grievance Content & Vault */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <span className="font-mono text-sm font-bold text-sky-800 bg-sky-50 px-2.5 py-1 rounded-lg border border-sky-200">
                  #{complaint.id}
                </span>
                <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-slate-100 text-slate-800">
                  {complaint.status.replace(/_/g, ' ')}
                </span>
              </div>

              {/* Raw Vault Clearance Button for Officers */}
              {role !== 'citizen' && (
                <button
                  onClick={() => setShowRaw(!showRaw)}
                  className="flex items-center space-x-1 px-3 py-1 bg-slate-100 hover:bg-slate-200 rounded-lg text-xs font-semibold text-slate-700 transition"
                >
                  {showRaw ? <Unlock className="w-3.5 h-3.5 text-amber-600" /> : <Lock className="w-3.5 h-3.5 text-slate-500" />}
                  <span>{showRaw ? 'Mask PII' : 'View Raw Vault'}</span>
                </button>
              )}
            </div>

            <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block">
                {showRaw ? 'Restricted Citizen Input (Unmasked)' : 'Sanitized Complaint (PII Protected)'}
              </span>
              <p className="text-sm text-slate-800 leading-relaxed font-medium">
                {showRaw ? (complaint.raw_content || complaint.redacted_content) : complaint.redacted_content}
              </p>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
              <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200">
                <span className="text-slate-500 block text-[10px]">Department</span>
                <span className="font-bold text-slate-900">{complaint.department || 'Unassigned'}</span>
              </div>
              <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200">
                <span className="text-slate-500 block text-[10px]">Priority</span>
                <span className="font-bold text-slate-900">{complaint.priority}</span>
              </div>
              <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200">
                <span className="text-slate-500 block text-[10px]">Ward / Zone</span>
                <span className="font-bold text-slate-900">{complaint.ward || 'Ward 12'}</span>
              </div>
              <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200">
                <span className="text-slate-500 block text-[10px]">Language</span>
                <span className="font-bold text-slate-900">{complaint.original_language === 'ta' ? 'தமிழ் (TA)' : 'English (EN)'}</span>
              </div>
            </div>
          </div>

          {/* Card: Bounded AI Recommendation & Citations */}
          {rec && (
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
                  <Sparkles className="w-4 h-4 text-sky-600" />
                  <span>AI Triage Recommendation & Grounding</span>
                </h3>
                <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-sky-100 text-sky-800">
                  {(rec.confidence * 100).toFixed(0)}% Confidence
                </span>
              </div>

              <div className="p-4 bg-sky-50/50 rounded-xl border border-sky-100 space-y-2">
                <p className="text-xs text-slate-800">
                  Recommended Department: <strong>{rec.suggested_department}</strong> ({rec.priority_score} Priority)
                </p>
                <div className="space-y-1 text-xs text-slate-600">
                  {rec.reasons.map((r, i) => (
                    <p key={i}>&bull; {r}</p>
                  ))}
                </div>
              </div>

              {/* Citations Panel */}
              <PolicyCitationPanel citations={rec.citations} lang={lang} t={t} />

              {/* Action Buttons for Officers */}
              {role !== 'citizen' && (
                <div className="pt-2 flex items-center space-x-3">
                  <button
                    onClick={() => onOpenApproval(complaint)}
                    className="flex-1 py-2.5 px-4 bg-sky-600 hover:bg-sky-700 text-white rounded-xl text-xs font-bold shadow-sm transition flex items-center justify-center space-x-1.5"
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    <span>{t.officer.approveRouting}</span>
                  </button>

                  <button
                    onClick={() => onOpenResolution(complaint)}
                    className="flex-1 py-2.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold shadow-sm transition flex items-center justify-center space-x-1.5"
                  >
                    <ShieldCheck className="w-4 h-4" />
                    <span>{t.officer.checkResolution}</span>
                  </button>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right Col: Cryptographic Audit Trail & Evidence */}
        <div className="space-y-6">
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
            <AuditTimeline caseId={complaint.id} lang={lang} />
          </div>
        </div>
      </div>
    </div>
  );
};
