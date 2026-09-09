import React, { useState } from 'react';
import { Send, CheckCheck, Smartphone, Bot } from 'lucide-react';

interface ChatMessage {
  id: string;
  sender: 'bot' | 'user';
  text: string;
  time: string;
}

export const WhatsAppBotSimulator: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      sender: 'bot',
      text: 'வணக்கம்! Greater Chennai Corporation Civic WhatsApp Bot-க்கு வரவேற்கிறோம். புகாரை பதிவு செய்ய உங்கள் பிரச்சனையை தெரிவிக்கவும். (Please describe your civic issue)',
      time: '19:30',
    },
  ]);
  const [inputVal, setInputVal] = useState('');
  const [step, setStep] = useState(1);

  const handleSend = () => {
    if (!inputVal.trim()) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: inputVal,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    const currentInput = inputVal;
    setInputVal('');

    setTimeout(() => {
      let botReply = '';
      if (step === 1) {
        botReply = 'உங்கள் வார்டு எண் மற்றும் தெரு பெயரை குறிப்பிடவும் (Please provide Ward No. & Street name):';
        setStep(2);
      } else if (step === 2) {
        botReply = `நன்றி! உங்கள் புகார் பதிவு செய்யப்பட்டது. குறிப்பு எண்: #WA-${Math.floor(100000 + Math.random() * 900000)}. அதிகாரிக்கு அனுப்பப்பட்டது. (Complaint Registered & Dispatched!)`;
        setStep(3);
      } else {
        botReply = 'உங்கள் புகார் பரிசீலனையில் உள்ளது. நிலை அறிய STATUS என அனுப்பவும்.';
      }

      const botMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'bot',
        text: botReply,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, botMsg]);
    }, 500);
  };

  return (
    <div className="max-w-md mx-auto bg-slate-900 border border-slate-700 rounded-3xl overflow-hidden shadow-2xl flex flex-col h-[520px]">
      {/* WhatsApp Header */}
      <div className="bg-emerald-700 px-4 py-3 text-white flex items-center justify-between shadow-md">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-full bg-emerald-800 flex items-center justify-center border border-emerald-500">
            <Bot className="w-5 h-5 text-emerald-200" />
          </div>
          <div>
            <div className="text-xs font-bold flex items-center gap-1">
              GCC CivicBot 24/7
              <span className="w-2 h-2 rounded-full bg-emerald-300 inline-block" />
            </div>
            <div className="text-[10px] text-emerald-100">Official Municipal Channel</div>
          </div>
        </div>
        <Smartphone className="w-5 h-5 text-emerald-200" />
      </div>

      {/* Chat Messages Body */}
      <div className="flex-1 bg-[#0b141a] p-4 overflow-y-auto space-y-3">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex flex-col max-w-[82%] ${
              m.sender === 'user' ? 'ml-auto items-end' : 'mr-auto items-start'
            }`}
          >
            <div
              className={`p-3 rounded-2xl text-xs leading-relaxed ${
                m.sender === 'user'
                  ? 'bg-emerald-800 text-white rounded-tr-none'
                  : 'bg-slate-800 text-slate-100 rounded-tl-none border border-slate-700'
              }`}
            >
              {m.text}
              <div className="flex items-center justify-end gap-1 mt-1 text-[9px] text-slate-400">
                <span>{m.time}</span>
                {m.sender === 'user' && <CheckCheck className="w-3 h-3 text-cyan-400" />}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Prompts */}
      <div className="bg-slate-950 px-3 py-1.5 border-t border-slate-800 flex gap-1.5 overflow-x-auto">
        {['குடிநீர் கசிவு', 'தெருவிளக்கு எரியவில்லை', 'Pothole on Main Road'].map((sample) => (
          <button
            key={sample}
            onClick={() => setInputVal(sample)}
            className="text-[10px] bg-slate-800 text-slate-300 hover:text-white px-2 py-1 rounded-full whitespace-nowrap border border-slate-700 transition"
          >
            {sample}
          </button>
        ))}
      </div>

      {/* Input Bar */}
      <div className="bg-slate-900 p-2.5 border-t border-slate-800 flex items-center gap-2">
        <input
          type="text"
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type WhatsApp message..."
          className="flex-1 bg-slate-950 border border-slate-800 text-white rounded-full px-4 py-2 text-xs focus:outline-none focus:border-emerald-500"
        />
        <button
          onClick={handleSend}
          className="w-8 h-8 rounded-full bg-emerald-600 hover:bg-emerald-500 text-white flex items-center justify-center transition shadow-md"
        >
          <Send className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
