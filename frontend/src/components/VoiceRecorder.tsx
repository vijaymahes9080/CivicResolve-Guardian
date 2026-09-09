import React, { useState, useEffect } from 'react';
import { Mic, Square, CheckCircle2 } from 'lucide-react';

interface VoiceRecorderProps {
  onTranscriptionComplete?: (text: string) => void;
  lang?: 'en' | 'ta';
}

export const VoiceRecorder: React.FC<VoiceRecorderProps> = ({ onTranscriptionComplete, lang = 'ta' }) => {
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [recordTime, setRecordTime] = useState<number>(0);
  const [audioRecorded, setAudioRecorded] = useState<boolean>(false);
  const [transcribedText, setTranscribedText] = useState<string>('');

  useEffect(() => {
    let timer: any;
    if (isRecording) {
      timer = setInterval(() => setRecordTime((prev) => prev + 1), 1000);
    }
    return () => clearInterval(timer);
  }, [isRecording]);

  const handleStart = () => {
    setIsRecording(true);
    setRecordTime(0);
    setAudioRecorded(false);
    setTranscribedText('');
  };

  const handleStop = () => {
    setIsRecording(false);
    setAudioRecorded(true);
    // Simulate bilingual speech transcription
    const simulated = lang === 'ta'
      ? 'குடிநீர் குழாயில் விரிசல் ஏற்பட்டு மூன்று நாட்களாக சாலையில் தண்ணீர் வீணாக ஓடுகிறது.'
      : 'Main underground water pipe burst near door no 12, water flooding street since morning.';
    setTranscribedText(simulated);
    if (onTranscriptionComplete) {
      onTranscriptionComplete(simulated);
    }
  };

  const formatSeconds = (sec: number) => {
    const mins = Math.floor(sec / 60);
    const secs = sec % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className={`p-2 rounded-xl ${isRecording ? 'bg-rose-500/20 text-rose-400 animate-pulse' : 'bg-blue-500/20 text-blue-400'}`}>
            <Mic className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-sm font-bold text-white">
              {lang === 'ta' ? 'குரல் பதிவு (Tamil Voice Note)' : 'Voice Note Recording'}
            </h4>
            <p className="text-[11px] text-slate-400">
              {lang === 'ta' ? 'நேரடியாக பேசி உங்கள் புகாரை பதிவு செய்யவும்' : 'Speak to record your grievance directly'}
            </p>
          </div>
        </div>

        {isRecording && (
          <span className="text-xs font-mono font-bold text-rose-400 bg-rose-950/80 px-2.5 py-1 rounded-full border border-rose-500/40 animate-pulse">
            REC {formatSeconds(recordTime)}
          </span>
        )}
      </div>

      {/* Animated Waveform Visualizer */}
      <div className="h-16 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-center gap-1.5 px-4 overflow-hidden mb-4">
        {[20, 45, 75, 30, 90, 60, 80, 40, 95, 70, 50, 85, 35, 65, 40, 80, 55, 30, 90, 45].map((height, i) => (
          <div
            key={i}
            style={{
              height: isRecording ? `${Math.max(15, (height * (recordTime % 3 + 1)) % 90)}%` : '15%',
              transition: 'height 0.15s ease-in-out',
            }}
            className={`w-1.5 rounded-full ${
              isRecording
                ? 'bg-gradient-to-t from-blue-500 to-cyan-400 shadow-sm shadow-cyan-400/50'
                : audioRecorded
                ? 'bg-emerald-500'
                : 'bg-slate-800'
            }`}
          />
        ))}
      </div>

      {/* Control Buttons */}
      <div className="flex items-center gap-3">
        {!isRecording ? (
          <button
            type="button"
            onClick={handleStart}
            className="flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition shadow-lg shadow-blue-500/25"
          >
            <Mic className="w-4 h-4" />
            {audioRecorded
              ? (lang === 'ta' ? 'மீண்டும் பேசவும்' : 'Re-record Voice')
              : (lang === 'ta' ? 'குரல் பதிவை தொடங்குக' : 'Start Voice Input')}
          </button>
        ) : (
          <button
            type="button"
            onClick={handleStop}
            className="flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs transition shadow-lg shadow-rose-500/25 animate-pulse"
          >
            <Square className="w-4 h-4 fill-current" />
            {lang === 'ta' ? 'பதிவை முடிக்க' : 'Stop & Transcribe'}
          </button>
        )}
      </div>

      {/* Live AI Transcription Result */}
      {transcribedText && (
        <div className="mt-4 p-3 bg-emerald-950/30 border border-emerald-500/30 rounded-xl">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-400 mb-1">
            <CheckCircle2 className="w-4 h-4" />
            <span>{lang === 'ta' ? 'தானியங்கி உரை வடிவம் (Transcribed)' : 'AI Whisper Transcription'}</span>
          </div>
          <p className="text-xs text-slate-300 italic">"{transcribedText}"</p>
        </div>
      )}
    </div>
  );
};
