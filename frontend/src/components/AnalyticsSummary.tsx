import React from 'react';
import { BarChart3, Clock, CheckCircle2, AlertOctagon, TrendingUp, ShieldCheck } from 'lucide-react';

interface AnalyticsSummaryProps {
  lang: 'en' | 'ta';
  t: any;
}

export const AnalyticsSummary: React.FC<AnalyticsSummaryProps> = ({ lang, t }) => {
  const stats = [
    { label: lang === 'ta' ? 'மொத்த புகார்கள்' : 'Total Grievances', val: '1,428', change: '+12%', icon: <TrendingUp className="w-5 h-5 text-sky-600" /> },
    { label: lang === 'ta' ? 'SLA காலக்கெடு வெற்றி' : 'SLA Compliance Rate', val: '94.2%', change: '+3.1%', icon: <Clock className="w-5 h-5 text-emerald-600" /> },
    { label: lang === 'ta' ? 'உறுதி செய்யப்பட்ட தீர்வுகள்' : 'Verified Resolution Rate', val: '88.6%', change: '+4.5%', icon: <CheckCircle2 className="w-5 h-5 text-indigo-600" /> },
    { label: lang === 'ta' ? 'தடுக்கப்பட்ட தவறான தீர்வுகள்' : 'Contradictions Caught', val: '43', change: '-15%', icon: <AlertOctagon className="w-5 h-5 text-rose-600" /> }
  ];

  const depts = [
    { name: 'Water Supply & Sewerage', cases: 480, pct: 34, color: 'bg-sky-600' },
    { name: 'Roads & Bridges', cases: 390, pct: 27, color: 'bg-amber-600' },
    { name: 'Solid Waste Management', cases: 260, pct: 18, color: 'bg-emerald-600' },
    { name: 'Electrical & Lighting', cases: 188, pct: 13, color: 'bg-indigo-600' },
    { name: 'Public Health & Sanitation', cases: 110, pct: 8, color: 'bg-purple-600' },
  ];

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-slate-900">{t.nav.analytics}</h2>
        <p className="text-xs text-slate-500">Real-time municipal grievance resolution & SLA compliance metrics</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {stats.map((s, idx) => (
          <div key={idx} className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-500">{s.label}</span>
              <div className="p-2 bg-slate-50 rounded-lg">{s.icon}</div>
            </div>
            <div className="flex items-baseline space-x-2">
              <span className="text-2xl font-extrabold text-slate-900">{s.val}</span>
              <span className="text-xs font-semibold text-emerald-600">{s.change}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Department Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
            <BarChart3 className="w-4 h-4 text-sky-600" />
            <span>Department Grievance Load Distribution</span>
          </h3>

          <div className="space-y-3 pt-2">
            {depts.map((d, i) => (
              <div key={i} className="space-y-1 text-xs">
                <div className="flex justify-between text-slate-700">
                  <span className="font-semibold">{d.name}</span>
                  <span>{d.cases} cases ({d.pct}%)</span>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-100 overflow-hidden">
                  <div className={`h-full rounded-full ${d.color}`} style={{ width: `${d.pct}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Resolution Quality Audit Funnel */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Resolution Veracity Auditing</span>
          </h3>

          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs space-y-3">
            <p className="text-slate-600">
              CivicResolve Guardian continuously verifies that marked resolutions contain photographic proof, valid timestamps, and genuine remediation.
            </p>

            <div className="grid grid-cols-3 gap-2 text-center pt-2">
              <div className="p-3 bg-white rounded-lg border border-emerald-200">
                <span className="text-emerald-700 font-bold text-lg block">91.4%</span>
                <span className="text-[10px] text-slate-500 font-medium">Likely Resolved</span>
              </div>
              <div className="p-3 bg-white rounded-lg border border-amber-200">
                <span className="text-amber-700 font-bold text-lg block">5.6%</span>
                <span className="text-[10px] text-slate-500 font-medium">Evidence Gaps</span>
              </div>
              <div className="p-3 bg-white rounded-lg border border-rose-200">
                <span className="text-rose-700 font-bold text-lg block">3.0%</span>
                <span className="text-[10px] text-slate-500 font-medium">Contradictions</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
