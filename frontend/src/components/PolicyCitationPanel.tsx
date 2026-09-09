import React from 'react';
import { BookOpen, ShieldAlert, CheckCircle2, Clock, ArrowUpRight } from 'lucide-react';
import { PolicyCitation } from '../types';

interface PolicyCitationPanelProps {
  citations: PolicyCitation[];
  lang: 'en' | 'ta';
  t: any;
}

export const PolicyCitationPanel: React.FC<PolicyCitationPanelProps> = ({ citations, lang, t }) => {
  if (!citations || citations.length === 0) {
    return (
      <div className="p-4 bg-amber-50 rounded-xl border border-amber-200 text-xs text-amber-900 flex items-start space-x-2">
        <ShieldAlert className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
        <div>
          <p className="font-semibold">
            {lang === 'ta' ? 'நேரடி நகராட்சி விதி சான்றுகள் கிடைக்கவில்லை' : 'Insufficient Evidence Match'}
          </p>
          <p className="text-amber-800 mt-0.5">
            {lang === 'ta'
              ? 'இந்த புகாருக்கு நேரடி சட்ட விதி பொருந்தவில்லை. அதிகாரி தனது அதிகாரபூர்வ பரிசீலனையின் அடிப்படையில் முடிவு செய்ய வேண்டும்.'
              : 'No official municipal charter section matched the grievance claim above confidence threshold. Officer discretion required.'}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center space-x-1.5">
          <BookOpen className="w-4 h-4 text-sky-600" />
          <span>{lang === 'ta' ? 'அரசு சட்ட விதிகள் & சான்றுகள்' : 'Grounded Policy Citations'}</span>
        </h4>
        <span className="text-[10px] font-semibold bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full">
          {citations.length} {lang === 'ta' ? 'சான்றுகள் உறுதி செய்யப்பட்டது' : 'Verified Citations'}
        </span>
      </div>

      <div className="space-y-2.5">
        {citations.map((c, idx) => (
          <div
            key={idx}
            className="p-3.5 bg-slate-50 hover:bg-slate-100/80 rounded-xl border border-slate-200 transition"
          >
            <div className="flex items-start justify-between">
              <div>
                <span className="text-xs font-bold text-sky-900 block">{c.title}</span>
                <span className="text-[10px] font-mono text-slate-500">
                  {c.policy_id} &bull; Section {c.section_id}
                </span>
              </div>
              <span className="text-[10px] font-semibold bg-sky-100 text-sky-800 px-2 py-0.5 rounded-md">
                {(c.relevance_score * 100).toFixed(0)}% match
              </span>
            </div>

            <p className="text-xs text-slate-700 mt-2 bg-white p-2.5 rounded-lg border border-slate-200/80 italic">
              "{c.excerpt}"
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
