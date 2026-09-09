import React, { useState, useEffect } from 'react';
import { BookOpen, Search, Clock, AlertTriangle, ShieldCheck } from 'lucide-react';
import { PolicyCitation } from '../types';
import { api } from '../services/api';

interface PolicyExplorerProps {
  lang: 'en' | 'ta';
  t: any;
}

export const PolicyExplorer: React.FC<PolicyExplorerProps> = ({ lang, t }) => {
  const [query, setQuery] = useState('water contamination');
  const [citations, setCitations] = useState<PolicyCitation[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (q: string) => {
    if (!q || q.length < 3) return;
    setLoading(true);
    try {
      const data = await api.searchPolicies(q);
      setCitations(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleSearch(query);
  }, []);

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 space-y-4">
        <div className="flex items-center space-x-2">
          <BookOpen className="w-6 h-6 text-sky-600" />
          <h2 className="text-xl font-bold text-slate-900">{t.nav.policySearch}</h2>
        </div>
        <p className="text-xs text-slate-500">
          Search Tamil Nadu Municipal Bylaws, Citizen Charters, and SLA Regulations grounded in administrative law.
        </p>

        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch(query)}
            placeholder="e.g. drinking water contamination, pothole repair, garbage overflow, street light failure..."
            className="flex-1 rounded-xl border border-slate-300 px-4 py-2.5 text-xs text-slate-800 focus:ring-2 focus:ring-sky-500"
          />
          <button
            onClick={() => handleSearch(query)}
            disabled={loading}
            className="px-5 py-2.5 bg-sky-600 hover:bg-sky-700 text-white rounded-xl text-xs font-semibold shadow-sm transition"
          >
            {loading ? 'Searching...' : 'Search Bylaws'}
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {loading ? (
          <div className="p-12 text-center text-xs text-slate-500">Retrieving grounded policy sections...</div>
        ) : citations.length === 0 ? (
          <div className="p-8 bg-amber-50 rounded-2xl border border-amber-200 text-center text-xs text-amber-900">
            No matching municipal bylaws found above the 50% relevance threshold.
          </div>
        ) : (
          citations.map((c, i) => (
            <div key={i} className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-bold text-slate-900">{c.title}</h3>
                  <span className="text-[11px] font-mono text-sky-700">{c.policy_id}</span>
                </div>
                <span className="px-2.5 py-1 bg-emerald-50 text-emerald-700 font-bold text-xs rounded-full border border-emerald-200">
                  {(c.relevance_score * 100).toFixed(0)}% Relevance
                </span>
              </div>
              <p className="text-xs text-slate-700 italic bg-slate-50 p-3.5 rounded-xl border border-slate-200">
                "{c.excerpt}"
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
