import React, { useState } from 'react';
import { Mic, MicOff, ShieldCheck, UploadCloud, CheckCircle2, Eye, AlertTriangle } from 'lucide-react';
import { api } from '../services/api';
import { ComplaintRecord } from '../types';

interface CitizenFormProps {
  lang: 'en' | 'ta';
  t: any;
  onSubmitted: (complaint: ComplaintRecord) => void;
}

export const CitizenForm: React.FC<CitizenFormProps> = ({ lang, t, onSubmitted }) => {
  const [content, setContent] = useState('');
  const [ward, setWard] = useState('Ward 12');
  const [zone, setZone] = useState('Zone 4 (Central)');
  const [isRecording, setIsRecording] = useState(false);
  const [audioConsent, setAudioConsent] = useState(true);
  const [evidenceFile, setEvidenceFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [submittedCase, setSubmittedCase] = useState<ComplaintRecord | null>(null);
  const [showPiiPreview, setShowPiiPreview] = useState(false);

  // Simulated PII preview on client side
  const computePiiPreview = (text: string) => {
    return text
      .replace(/(?:\+91[\-\s]?)?[6-9]\d{9}\b/g, '[PHONE_REDACTED]')
      .replace(/\b[2-9]{1}\d{3}[\s\-]?[0-9]{4}[\s\-]?[0-9]{4}\b/g, '[AADHAAR_REDACTED]')
      .replace(/\b(?:door\s*no\.?|house\s*no\.?|d\.?no\.?|கதவு\s*எண்)\s*[:\-]?\s*[\w\-\/\#]+/gi, '[DOOR_ADDRESS_REDACTED]');
  };

  const handleToggleVoice = () => {
    if (!isRecording) {
      setIsRecording(true);
      // Simulate audio transcription
      setTimeout(() => {
        setIsRecording(false);
        const voiceText = lang === 'ta'
          ? 'எங்கள் பகுதியில் கதவு எண் 12, 4வது குறுக்குத் தெருவில் கடந்த மூன்று நாட்களாக குடிநீர் குழாய் உடைந்து குடிநீரில் கழிவுநீர் துர்நாற்றம் வீசுகிறது. தொடர்பு எண் 9840123456.'
          : 'Severe drinking water contamination at Door No. 14/2, 4th Cross Street, Ward 12. Heavy sewage smell since 3 days. Contact me at 9840123456.';
        setContent(voiceText);
      }, 3000);
    } else {
      setIsRecording(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) return;

    setSubmitting(true);
    try {
      const complaint = await api.createComplaint({
        content,
        language: lang,
        ward,
        zone,
        has_audio: false
      });

      if (evidenceFile) {
        await api.uploadEvidence(complaint.id, evidenceFile, 'Initial citizen evidence photo');
      }

      setSubmittedCase(complaint);
      onSubmitted(complaint);
    } catch (err: any) {
      alert(`Submission error: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-8 px-4 sm:px-6">
      <div className="bg-white rounded-2xl shadow-xl shadow-slate-200/60 border border-slate-200/80 overflow-hidden">
        {/* Card Header */}
        <div className="bg-gradient-to-r from-sky-900 via-sky-800 to-indigo-900 p-6 text-white">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 bg-white/10 rounded-xl backdrop-blur">
              <ShieldCheck className="w-6 h-6 text-sky-300" />
            </div>
            <div>
              <h2 className="text-xl font-bold">{t.citizen.title}</h2>
              <p className="text-xs text-sky-200">{t.citizen.subtitle}</p>
            </div>
          </div>
        </div>

        {submittedCase ? (
          <div className="p-8 text-center space-y-4">
            <div className="w-16 h-16 mx-auto bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600">
              <CheckCircle2 className="w-10 h-10" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">{t.citizen.successMessage}</h3>
            <p className="font-mono text-sm bg-slate-100 py-2 px-4 rounded-lg inline-block text-sky-800 font-semibold select-all">
              {submittedCase.id}
            </p>
            <div className="p-4 bg-sky-50 rounded-xl border border-sky-200 text-left text-xs text-sky-900 space-y-1">
              <p><strong>{lang === 'ta' ? 'பாதுகாக்கப்பட்ட புகார் உரை:' : 'Sanitized Redacted Grievance:'}</strong></p>
              <p className="italic text-slate-700">{submittedCase.redacted_content}</p>
              <p className="text-[11px] text-emerald-700 pt-2 flex items-center">
                <ShieldCheck className="w-3.5 h-3.5 mr-1" />
                {lang === 'ta' ? 'தனிநபர் விவரங்கள் வெற்றிகரமாக மறைக்கப்பட்டது.' : 'PII entities successfully quarantined in Restricted Vault.'}
              </p>
            </div>
            <button
              onClick={() => { setSubmittedCase(null); setContent(''); }}
              className="mt-4 px-6 py-2 bg-sky-600 hover:bg-sky-700 text-white rounded-lg text-sm font-semibold transition"
            >
              {lang === 'ta' ? 'மற்றொரு புகாரைப் பதிவுசெய்க' : 'File Another Grievance'}
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="p-6 sm:p-8 space-y-6">
            {/* Privacy Guarantee Alert */}
            <div className="p-3.5 bg-sky-50/80 rounded-xl border border-sky-200 text-xs text-sky-900 flex items-start space-x-2.5">
              <ShieldCheck className="w-5 h-5 text-sky-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold">{t.citizen.piiDisclosure}</p>
              </div>
            </div>

            {/* Content Textarea & Voice Button */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="text-sm font-semibold text-slate-800">
                  {t.citizen.contentLabel} <span className="text-rose-500">*</span>
                </label>
                <button
                  type="button"
                  onClick={handleToggleVoice}
                  className={`flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-semibold transition ${
                    isRecording
                      ? 'bg-rose-100 text-rose-700 animate-pulse border border-rose-300'
                      : 'bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border border-indigo-200'
                  }`}
                >
                  {isRecording ? <MicOff className="w-3.5 h-3.5" /> : <Mic className="w-3.5 h-3.5" />}
                  <span>{isRecording ? t.citizen.stopVoice : t.citizen.voiceInput}</span>
                </button>
              </div>

              <textarea
                id="complaint-content-input"
                rows={4}
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder={t.citizen.contentPlaceholder}
                required
                className="w-full rounded-xl border border-slate-300 p-3.5 text-sm text-slate-800 focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition placeholder:text-slate-400"
              />

              {content.length > 5 && (
                <div className="flex justify-end">
                  <button
                    type="button"
                    onClick={() => setShowPiiPreview(!showPiiPreview)}
                    className="text-xs text-sky-700 hover:text-sky-900 flex items-center space-x-1 font-medium"
                  >
                    <Eye className="w-3.5 h-3.5" />
                    <span>{showPiiPreview ? 'Hide Redaction Preview' : t.citizen.previewPII}</span>
                  </button>
                </div>
              )}

              {showPiiPreview && (
                <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs text-slate-600">
                  <span className="font-semibold text-slate-800 block mb-1">Live Privacy Preview:</span>
                  <p className="font-mono bg-white p-2 rounded border border-slate-200 text-slate-700">
                    {computePiiPreview(content)}
                  </p>
                </div>
              )}
            </div>

            {/* Ward & Zone Selection */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-semibold text-slate-700 block mb-1">
                  {t.citizen.wardLabel}
                </label>
                <select
                  value={ward}
                  onChange={(e) => setWard(e.target.value)}
                  className="w-full rounded-lg border border-slate-300 p-2.5 text-sm text-slate-800 focus:ring-2 focus:ring-sky-500"
                >
                  <option value="Ward 12">Ward 12 - Mylapore / Central</option>
                  <option value="Ward 14">Ward 14 - T. Nagar / South</option>
                  <option value="Ward 25">Ward 25 - Anna Nagar / West</option>
                  <option value="Ward 08">Ward 08 - George Town / North</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-700 block mb-1">
                  {t.citizen.zoneLabel}
                </label>
                <select
                  value={zone}
                  onChange={(e) => setZone(e.target.value)}
                  className="w-full rounded-lg border border-slate-300 p-2.5 text-sm text-slate-800 focus:ring-2 focus:ring-sky-500"
                >
                  <option value="Zone 4 (Central)">Zone 4 (Central)</option>
                  <option value="Zone 5 (South)">Zone 5 (South)</option>
                  <option value="Zone 3 (North)">Zone 3 (North)</option>
                  <option value="Zone 6 (East)">Zone 6 (East)</option>
                </select>
              </div>
            </div>

            {/* Evidence Attachment Upload */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-700 block">
                {lang === 'ta' ? 'புகைப்படச் சான்று இணைக்கவும் (விருப்பமானது)' : 'Attach Photo Evidence (Optional)'}
              </label>
              <div className="flex items-center space-x-3">
                <label className="cursor-pointer flex items-center space-x-2 px-4 py-2 border border-slate-300 rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-50 transition">
                  <UploadCloud className="w-4 h-4 text-slate-500" />
                  <span>{evidenceFile ? evidenceFile.name : (lang === 'ta' ? 'கோப்பைத் தேர்ந்தெடு' : 'Choose Image / PDF')}</span>
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
                {evidenceFile && (
                  <button
                    type="button"
                    onClick={() => setEvidenceFile(null)}
                    className="text-xs text-rose-600 hover:underline"
                  >
                    Remove
                  </button>
                )}
              </div>
            </div>

            {/* Submit Button */}
            <div className="pt-2">
              <button
                id="submit-complaint-btn"
                type="submit"
                disabled={submitting || !content.trim()}
                className="w-full py-3.5 px-4 rounded-xl bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-700 hover:to-indigo-700 text-white font-semibold text-sm shadow-md shadow-sky-600/25 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {submitting ? t.citizen.submitting : t.citizen.submitBtn}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
