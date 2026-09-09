import React from 'react';
import { IndianRupee, Wrench, Users, PackageCheck, AlertCircle } from 'lucide-react';

interface CostEstimatorProps {
  category: string;
  priority: string;
}

export const CostEstimatorCard: React.FC<CostEstimatorProps> = ({ category, priority }) => {
  const getSorData = () => {
    switch (category.toUpperCase()) {
      case 'WATER_SUPPLY':
        return {
          equipment: ['Super Sucker Jetting Machine', 'Dewatering Submersible Pump'],
          manpower: ['Junior Hydraulic Engineer (1)', 'Plumbing Crew (4)'],
          materials: 'UPVC High-Pressure Pipe & Collar Joint (6m)',
          equipmentCost: 7500,
          manpowerCost: 5700,
          materialCost: 3400,
          hours: 6.0,
        };
      case 'SOLID_WASTE':
        return {
          equipment: ['Compactor Garbage Truck', 'Mechanical Sweeper'],
          manpower: ['Sanitary Inspector (1)', 'Sanitation Workers (4)'],
          materials: 'Bio-sanitizing Disinfectant Solution (50L)',
          equipmentCost: 2975,
          manpowerCost: 2450,
          materialCost: 1800,
          hours: 3.5,
        };
      case 'ROAD_TRANSPORT':
        return {
          equipment: ['Tandem Vibratory Road Roller', 'Bitumen Sprayer', 'JCB Backhoe Loader'],
          manpower: ['Assistant Engineer PWD (1)', 'Asphalt Operators (2)', 'Paving Crew (4)'],
          materials: 'Dense Bituminous Macadam Cold Mix (2.5T)',
          equipmentCost: 16800,
          manpowerCost: 11200,
          materialCost: 11500,
          hours: 8.0,
        };
      default:
        return {
          equipment: ['Hydraulic Sky Lift Crane'],
          manpower: ['Certified Lineman Electrician (2)'],
          materials: '65W LED Luminaire + Photocell Sensor',
          equipmentCost: 2250,
          manpowerCost: 1500,
          materialCost: 4200,
          hours: 2.5,
        };
    }
  };

  const data = getSorData();
  const mult = priority.toLowerCase() === 'critical' ? 1.5 : 1.0;
  const totalInr = Math.round((data.equipmentCost + data.manpowerCost + data.materialCost) * mult);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 text-white">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-amber-500/20 text-amber-400">
            <IndianRupee className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-xs font-bold text-white uppercase tracking-wider">
              PWD Schedule of Rates (SOR) Resource Estimate
            </h4>
            <span className="text-[10px] text-slate-400">Reference: PWD-TN-SOR-2025-26</span>
          </div>
        </div>

        <span className="text-xs font-bold font-mono text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-500/30">
          ₹ {totalInr.toLocaleString('en-IN')}
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
        {/* Equipment */}
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
          <div className="flex items-center gap-1.5 text-slate-400 font-semibold mb-1">
            <Wrench className="w-3.5 h-3.5 text-cyan-400" /> Equipment
          </div>
          <ul className="text-[11px] text-slate-300 space-y-0.5">
            {data.equipment.map((eq, i) => (
              <li key={i}>• {eq}</li>
            ))}
          </ul>
        </div>

        {/* Manpower */}
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
          <div className="flex items-center gap-1.5 text-slate-400 font-semibold mb-1">
            <Users className="w-3.5 h-3.5 text-blue-400" /> Workforce
          </div>
          <ul className="text-[11px] text-slate-300 space-y-0.5">
            {data.manpower.map((mp, i) => (
              <li key={i}>• {mp}</li>
            ))}
          </ul>
        </div>

        {/* Materials */}
        <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80">
          <div className="flex items-center gap-1.5 text-slate-400 font-semibold mb-1">
            <PackageCheck className="w-3.5 h-3.5 text-emerald-400" /> Materials
          </div>
          <p className="text-[11px] text-slate-300">{data.materials}</p>
        </div>
      </div>

      <div className="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
        <span>Est. Repair Duration: <strong className="text-white">{data.hours * mult} hrs</strong></span>
        <span>
          Sanction Level: <strong className="text-amber-300">{totalInr > 20000 ? 'Assistant Exec. Engineer (AEE)' : 'Junior Engineer (JE)'}</strong>
        </span>
      </div>
    </div>
  );
};
