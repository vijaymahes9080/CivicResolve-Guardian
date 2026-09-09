import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { CitizenForm } from './components/CitizenForm';
import { OfficerQueue } from './components/OfficerQueue';
import { CaseTracker } from './components/CaseTracker';
import { CaseDetail } from './components/CaseDetail';
import { ApprovalDrawer } from './components/ApprovalDrawer';
import { ResolutionAuditModal } from './components/ResolutionAuditModal';
import { PolicyExplorer } from './components/PolicyExplorer';
import { AnalyticsSummary } from './components/AnalyticsSummary';
import { ComplaintRecord } from './types';
import { api } from './services/api';

import en from './i18n/en.json';
import ta from './i18n/ta.json';

export const App: React.FC = () => {
  const [lang, setLang] = useState<'en' | 'ta'>('en');
  const [activeTab, setActiveTab] = useState<'citizen' | 'tracker' | 'officer' | 'policies' | 'analytics'>('citizen');
  const [role, setRole] = useState<'citizen' | 'officer' | 'admin'>('citizen');
  
  const [selectedCase, setSelectedCase] = useState<ComplaintRecord | null>(null);
  const [approvalCase, setApprovalCase] = useState<ComplaintRecord | null>(null);
  const [resolutionCase, setResolutionCase] = useState<ComplaintRecord | null>(null);
  const [trackedCaseId, setTrackedCaseId] = useState<string>('');

  const t = lang === 'ta' ? ta : en;

  // Handle role switch & re-auth
  useEffect(() => {
    api.authenticate(role);
  }, [role]);

  const handleCaseSubmitted = (complaint: ComplaintRecord) => {
    setTrackedCaseId(complaint.id);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-['Outfit',sans-serif]">
      {/* Top Banner Notice */}
      <div className="bg-slate-900 text-slate-300 text-[11px] py-1.5 px-4 text-center border-b border-slate-800 flex items-center justify-center space-x-2">
        <span className="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
        <span>
          {lang === 'ta'
            ? 'சிவிக்ரிசால்வ் கார்டியன் - நேரடி மனித மேற்பார்வை & தகவல் பாதுகாப்பு முறை இயக்கத்தில் உள்ளது.'
            : 'CivicResolve Guardian Production Mode: Dual-Storage Privacy & Bounded Human-in-the-Loop Gating Active.'}
        </span>
      </div>

      {/* Main Navigation */}
      <Navbar
        lang={lang}
        setLang={setLang}
        activeTab={activeTab}
        setActiveTab={(tab: any) => {
          setSelectedCase(null);
          setActiveTab(tab);
        }}
        role={role}
        setRole={setRole}
        t={t}
      />

      {/* Main Content Body */}
      <main className="flex-1">
        {selectedCase ? (
          <CaseDetail
            complaint={selectedCase}
            onBack={() => setSelectedCase(null)}
            onOpenApproval={(c) => setApprovalCase(c)}
            onOpenResolution={(c) => setResolutionCase(c)}
            lang={lang}
            t={t}
            role={role}
          />
        ) : (
          <>
            {activeTab === 'citizen' && (
              <CitizenForm lang={lang} t={t} onSubmitted={handleCaseSubmitted} />
            )}

            {activeTab === 'tracker' && (
              <CaseTracker initialCaseId={trackedCaseId} lang={lang} t={t} />
            )}

            {activeTab === 'officer' && (
              <OfficerQueue
                onSelectCase={(c) => setSelectedCase(c)}
                onOpenApproval={(c) => setApprovalCase(c)}
                onOpenResolution={(c) => setResolutionCase(c)}
                lang={lang}
                t={t}
              />
            )}

            {activeTab === 'policies' && (
              <PolicyExplorer lang={lang} t={t} />
            )}

            {activeTab === 'analytics' && (
              <AnalyticsSummary lang={lang} t={t} />
            )}
          </>
        )}
      </main>

      {/* Modals & Drawers */}
      {approvalCase && (
        <ApprovalDrawer
          complaint={approvalCase}
          isOpen={!!approvalCase}
          onClose={() => setApprovalCase(null)}
          onApproved={(updated) => {
            if (selectedCase?.id === updated.id) setSelectedCase(updated);
            setApprovalCase(null);
          }}
          lang={lang}
          t={t}
        />
      )}

      {resolutionCase && (
        <ResolutionAuditModal
          complaint={resolutionCase}
          isOpen={!!resolutionCase}
          onClose={() => setResolutionCase(null)}
          onVerified={(updated) => {
            if (selectedCase?.id === updated.id) setSelectedCase(updated);
            setResolutionCase(null);
          }}
          lang={lang}
          t={t}
        />
      )}

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-6 px-4 text-center text-xs text-slate-500">
        <p>
          &copy; 2026 <strong>CivicResolve Guardian</strong> &bull; Tamil Nadu Urban Municipal Governance Platform &bull; Vijay Mahes
        </p>
        <p className="text-[11px] text-slate-400 mt-1">
          Built with FastAPI &bull; React &bull; Vite &bull; TypeScript &bull; MCP &bull; n8n
        </p>
      </footer>
    </div>
  );
};
export default App;
