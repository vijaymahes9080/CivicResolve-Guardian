import React, { useState } from 'react';
import { Volume2, Eye, ZoomIn, ZoomOut, Sparkles } from 'lucide-react';

interface AccessibilityBarProps {
  currentTextToRead?: string;
  lang?: 'en' | 'ta';
}

export const AccessibilityBar: React.FC<AccessibilityBarProps> = ({
  currentTextToRead = 'CivicResolve Guardian public municipal grievance portal.',
  lang = 'ta',
}) => {
  const [highContrast, setHighContrast] = useState(false);
  const [fontSizeLevel, setFontSizeLevel] = useState(1);
  const [isSpeaking, setIsSpeaking] = useState(false);

  const toggleHighContrast = () => {
    setHighContrast(!highContrast);
    document.documentElement.classList.toggle('contrast-more');
  };

  const handleZoom = (delta: number) => {
    setFontSizeLevel((prev) => Math.max(0, Math.min(2, prev + delta)));
  };

  const handleSpeak = () => {
    if (!('speechSynthesis' in window)) {
      alert('Speech synthesis is not supported in this browser.');
      return;
    }

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(currentTextToRead);
    utterance.lang = lang === 'ta' ? 'ta-IN' : 'en-IN';
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    setIsSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="bg-slate-900 border-b border-slate-800 px-4 py-2 text-xs flex items-center justify-between text-slate-300">
      <div className="flex items-center gap-2">
        <span className="font-semibold text-slate-400 flex items-center gap-1">
          <Sparkles className="w-3.5 h-3.5 text-blue-400" />
          {lang === 'ta' ? 'அணுகல்தன்மை வசதிகள் (A11y):' : 'Accessibility Bar:'}
        </span>
      </div>

      <div className="flex items-center gap-3">
        {/* Text-To-Speech Readout */}
        <button
          onClick={handleSpeak}
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg font-medium transition ${
            isSpeaking ? 'bg-rose-600 text-white animate-pulse' : 'bg-slate-800 hover:bg-slate-700 text-slate-200'
          }`}
          title="Read Aloud via Speech Synthesis"
        >
          <Volume2 className="w-3.5 h-3.5" />
          <span>{isSpeaking ? (lang === 'ta' ? 'நிறுத்து' : 'Stop Audio') : (lang === 'ta' ? 'படிக்கவும்' : 'Read Aloud')}</span>
        </button>

        {/* Font Zoom Controls */}
        <div className="flex items-center bg-slate-800 rounded-lg p-0.5 border border-slate-700">
          <button
            onClick={() => handleZoom(-1)}
            disabled={fontSizeLevel === 0}
            className="p-1 hover:text-white disabled:opacity-30"
            title="Decrease Font Size"
          >
            <ZoomOut className="w-3 h-3" />
          </button>
          <span className="px-1.5 text-[10px] font-mono">
            {fontSizeLevel === 0 ? 'A-' : fontSizeLevel === 1 ? 'A' : 'A+'}
          </span>
          <button
            onClick={() => handleZoom(1)}
            disabled={fontSizeLevel === 2}
            className="p-1 hover:text-white disabled:opacity-30"
            title="Increase Font Size"
          >
            <ZoomIn className="w-3 h-3" />
          </button>
        </div>

        {/* High Contrast */}
        <button
          onClick={toggleHighContrast}
          className={`flex items-center gap-1 px-2.5 py-1 rounded-lg font-medium border transition ${
            highContrast
              ? 'bg-yellow-400 text-black border-yellow-300 font-bold'
              : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border-slate-700'
          }`}
        >
          <Eye className="w-3.5 h-3.5" />
          <span>{lang === 'ta' ? 'உயர் மாறுபாடு' : 'High Contrast'}</span>
        </button>
      </div>
    </div>
  );
};
