import React, { useState } from 'react';
import { X, CheckCircle, AlertOctagon, HelpCircle, ShieldCheck, UploadCloud, FileCheck } from 'lucide-react';
import { ComplaintRecord, ResolutionAssessment } from '../types';
import { api } from '../services/api';

interface ResolutionAuditModalProps {
  complaint: ComplaintRecord;
  isOpen: boolean;
  onClose: () => void;
  onVerified: (complaint: ComplaintRecord) => void;
  lang: 'en' | 'ta';
  t: any;
}

export const ResolutionAuditModal: React.FC<ResolutionAuditModalProps> = ({
  complaint,
  isOpen,
  onClose,
  onVerified,
  lang,
  t
}) => {
  const [actionSummary, setActionSummary] = useState('');
  const [completionNotes, setCompletionNotes] = useState('');
  const [evidenceFile, setEvidenceFile] = useState<File | null>(null);
  const [evaluating, setEvaluating] = useState(false);
  const [assessment, setAssessment] = useState<ResolutionAssessment | null>(null);

  if (!isOpen) return null;

  const handleEvaluate = async () => {
    if (!actionSummary.trim()) return;
    setEvaluating(true);
    try {
      if (evidenceFile) {
        await api.uploadEvidence(complaint.id, evidenceFile, 'Officer resolution proof photo');
      }

      const res = await api.evaluateResolution(complaint.id, {
        action_taken_summary: actionSummary,
        completion_notes: completionNotes || undefined
      });

      setAssessment(res);
      const updated = await api.getComplaint(complaint.id);
      onVerified(updated);
    } catch (err: any) {
      alert(`Evaluation error: ${err.message}`);
    } finally {
      setEvaluating(false);
    }
  };

  const getVerdictBadge = (verdict: string) => {
    switch (verdict) {
      case 'likely_resolved':
        return {
          bg: 'bg-emerald-100 text-emerald-800 border-emerald-300',
          icon: <CheckCircle className="w-5 h-5 text-emerald-600" />,
          label: t.resolution.likelyResolved
        };
      case 'contradiction_detected':
        return {
          bg: 'bg-rose-100 text-rose-800 border-rose-300',
          icon: <AlertOctagon className="w-5 h-5 text-rose-600" />,
          label: t.resolution.contradictionDetected
        };
      case 'insufficient_evidence':
        return {
          bg: 'bg-amber-100 text-amber-800 border-amber-300',
          icon: <HelpCircle className="w-5 h-5 text-amber-600" />,
          label: t.resolution.insufficientEvidence
        };
      default:
        return {
          bg: 'bg-slate-100 text-slate-800 border-slate-300',
          icon: <HelpCircle className="w-5 h-5 text-slate-600" />,
          label: t.resolution.weakResolution
        };
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-xl w-full overflow-hidden border border-slate-200">
        {/* Modal Header */}
        <div className="bg-slate-900 p-5 text-white flex items-center justify-between">
          <div className="flex items-center space-x-2.5">
            <FileCheck className="w-5 h-5 text-sky-400" />
            <div>
              <h3 className="text-base font-bold">{t.resolution.modalTitle}</h3>
              <p className="text-xs text-slate-400">Case ID: {complaint.id.slice(0, 13)}...</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-5">
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs">
            <span className="font-semibold text-slate-600 block mb-1">Grievance Defect Reference:</span>
            <p className="text-slate-800 italic">"{complaint.redacted_content}"</p>
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-800 block">
              {t.resolution.actionSummary} <span className="text-rose-500">*</span>
            </label>
            <textarea
              id="action-summary-input"
              rows={3}
              value={actionSummary}
              onChange={(e) => setActionSummary(e.target.value)}
              placeholder={t.resolution.actionPlaceholder}
              className="w-full rounded-xl border border-slate-300 p-3 text-xs text-slate-800 focus:ring-sky-500"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-800 block">
              {t.resolution.completionNotes}
            </label>
            <input
              type="text"
              value={completionNotes}
              onChange={(e) => setCompletionNotes(e.target.value)}
              placeholder="e.g. Work inspected by AE Roads; road opened for normal transit."
              className="w-full rounded-lg border border-slate-300 p-2.5 text-xs focus:ring-sky-500"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-800 block">
              {t.resolution.attachProof}
            </label>
            <label className="cursor-pointer flex items-center space-x-2 px-4 py-2 border border-slate-300 rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-50 transition w-full">
              <UploadCloud className="w-4 h-4 text-slate-500" />
              <span className="truncate">{evidenceFile ? evidenceFile.name : 'Choose completion photo (e.g. pothole_patched.jpg)'}</span>
              <input
                type="file"
                accept="image/*,.pdf"
                className="hidden"
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    setEvidenceFile(e.target.files[0]);
                  }
                }}
              />
            </label>
          </div>

          {assessment && (
            <div className={`p-4 rounded-xl border-2 ${getVerdictBadge(assessment.evaluation_verdict).bg} space-y-2`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  {getVerdictBadge(assessment.evaluation_verdict).icon}
                  <span className="text-xs font-bold uppercase tracking-wider">
                    {getVerdictBadge(assessment.evaluation_verdict).label}
                  </span>
                </div>
                <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-white/70">
                  {(assessment.confidence * 100).toFixed(0)}% Confidence
                </span>
              </div>
              <p className="text-xs">{assessment.explanation}</p>
              {assessment.contradiction_notes && (
                <p className="text-xs font-semibold text-rose-800">
                  ⚠️ {assessment.contradiction_notes}
                </p>
              )}
            </div>
          )}

          <div className="flex items-center space-x-3 pt-2">
            <button
              id="evaluate-resolution-btn"
              onClick={handleEvaluate}
              disabled={evaluating || !actionSummary.trim()}
              className="flex-1 py-3 px-4 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl shadow transition disabled:opacity-50"
            >
              {evaluating ? 'Auditing Resolution...' : t.resolution.evaluateBtn}
            </button>
            <button
              onClick={onClose}
              className="px-5 py-3 border border-slate-300 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-50"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
