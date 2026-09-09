import React from 'react';
import { Shield, Globe, UserCheck, AlertCircle, Sparkles } from 'lucide-react';

interface NavbarProps {
  lang: 'en' | 'ta';
  setLang: (l: 'en' | 'ta') => void;
  activeTab: string;
  setActiveTab: (t: string) => void;
  role: 'citizen' | 'officer' | 'admin';
  setRole: (r: 'citizen' | 'officer' | 'admin') => void;
  t: any;
}

export const Navbar: React.FC<NavbarProps> = ({
  lang,
  setLang,
  activeTab,
  setActiveTab,
  role,
  setRole,
  t
}) => {
  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo & Name */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('citizen')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-sky-500/20">
              <Shield className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
                CivicResolve
              </span>
              <span className="text-xs ml-1.5 px-2 py-0.5 rounded-full font-semibold bg-sky-100 text-sky-800 border border-sky-200">
                Guardian
              </span>
              <p className="text-[11px] text-slate-500 hidden sm:block">
                {lang === 'ta' ? 'தமிழ்நாடு நகராட்சி குறைதீர்ப்பு தளம்' : 'Municipal Grievance Platform'}
              </p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center space-x-1" aria-label="Main Navigation">
            <button
              id="nav-file-complaint"
              onClick={() => setActiveTab('citizen')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                activeTab === 'citizen'
                  ? 'bg-sky-50 text-sky-700 font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              {t.nav.fileComplaint}
            </button>
            <button
              id="nav-track-case"
              onClick={() => setActiveTab('tracker')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                activeTab === 'tracker'
                  ? 'bg-sky-50 text-sky-700 font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              {t.nav.trackCase}
            </button>
            <button
              id="nav-officer-queue"
              onClick={() => setActiveTab('officer')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                activeTab === 'officer'
                  ? 'bg-sky-50 text-sky-700 font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              {t.nav.officerQueue}
            </button>
            <button
              id="nav-policies"
              onClick={() => setActiveTab('policies')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                activeTab === 'policies'
                  ? 'bg-sky-50 text-sky-700 font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              {t.nav.policySearch}
            </button>
            <button
              id="nav-analytics"
              onClick={() => setActiveTab('analytics')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition ${
                activeTab === 'analytics'
                  ? 'bg-sky-50 text-sky-700 font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              {t.nav.analytics}
            </button>
          </nav>

          {/* Controls: Language Toggle & Role Switcher */}
          <div className="flex items-center space-x-3">
            {/* Language Toggle */}
            <button
              id="lang-toggle-btn"
              onClick={() => setLang(lang === 'en' ? 'ta' : 'en')}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 text-xs font-semibold text-slate-700 transition"
              title="Toggle English / தமிழ்"
              aria-label="Toggle language"
            >
              <Globe className="w-3.5 h-3.5 text-sky-600" />
              <span>{lang === 'en' ? 'தமிழ் (TA)' : 'English (EN)'}</span>
            </button>

            {/* Role Switcher */}
            <div className="flex items-center space-x-1 bg-slate-100 p-1 rounded-lg border border-slate-200">
              <UserCheck className="w-3.5 h-3.5 ml-1.5 text-slate-500" />
              <select
                id="role-select"
                value={role}
                onChange={(e) => setRole(e.target.value as any)}
                className="bg-transparent text-xs font-semibold text-slate-800 pr-1 py-1 focus:outline-none cursor-pointer"
                aria-label="Switch simulated role"
              >
                <option value="citizen">Citizen</option>
                <option value="officer">Officer (GRO)</option>
                <option value="admin">Commissioner</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
