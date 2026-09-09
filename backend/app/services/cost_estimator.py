"""
CivicResolve Guardian - Municipal Resource & PWD Repair Cost Estimator
Calculates equipment, manpower, material requirements, and estimated expenditure
based on Tamil Nadu Public Works Department (PWD) Schedule of Rates (SOR).
"""

from typing import Dict, Any


PWD_SCHEDULE_OF_RATES = {
    "WATER_SUPPLY": {
        "equipment": ["Super Sucker Jetting Machine", "Dewatering Submersible Pump"],
        "equipment_rate_per_hr": 1250.0,
        "manpower": ["Junior Hydraulic Engineer (1)", "Plumbing Technicians (2)", "Civic Laborers (2)"],
        "manpower_rate_per_hr": 950.0,
        "base_material": "UPVC High-Pressure Pipe & Collar Joint",
        "material_unit_cost": 3400.0,
        "base_hours": 6.0,
    },
    "SOLID_WASTE": {
        "equipment": ["Compactor Garbage Truck", "Mechanical Road Sweeper"],
        "equipment_rate_per_hr": 850.0,
        "manpower": ["Sanitary Inspector (1)", "Sanitation Workers (4)"],
        "manpower_rate_per_hr": 700.0,
        "base_material": "Bio-sanitizing Disinfectant Spray (50L)",
        "material_unit_cost": 1800.0,
        "base_hours": 3.5,
    },
    "ROAD_TRANSPORT": {
        "equipment": ["Tandem Vibratory Road Roller", "Bitumen Sprayer", "JCB Backhoe Loader"],
        "equipment_rate_per_hr": 2100.0,
        "manpower": ["Assistant Engineer PWD (1)", "Asphalt Operators (2)", "Paving Crew (4)"],
        "manpower_rate_per_hr": 1400.0,
        "base_material": "Dense Bituminous Macadam (DBM Cold Mix 2.5T)",
        "material_unit_cost": 11500.0,
        "base_hours": 8.0,
    },
    "STREET_LIGHTING": {
        "equipment": ["Hydraulic Aerial Sky Lift Crane"],
        "equipment_rate_per_hr": 900.0,
        "manpower": ["TNEB Certified Electrician (1)", "Lineman Helper (1)"],
        "manpower_rate_per_hr": 600.0,
        "base_material": "65W Warm White LED Luminaire + Photocell Sensor",
        "material_unit_cost": 4200.0,
        "base_hours": 2.5,
    },
    "PUBLIC_HEALTH": {
        "equipment": ["Thermal Fogging Pulse Jet Machine", "Larvicide Sprayer"],
        "equipment_rate_per_hr": 650.0,
        "manpower": ["Health Inspector (1)", "Field Fumigators (2)"],
        "manpower_rate_per_hr": 550.0,
        "base_material": "Pyrethrum Extract & Abate Vector Larvicide",
        "material_unit_cost": 2200.0,
        "base_hours": 4.0,
    },
}


class MunicipalCostEstimator:
    """Provides automated municipal resource budgeting for public works departments."""

    @classmethod
    def estimate_repair(cls, category: str, priority: str = "medium") -> Dict[str, Any]:
        spec = PWD_SCHEDULE_OF_RATES.get(category.upper(), PWD_SCHEDULE_OF_RATES["ROAD_TRANSPORT"])

        priority_multipliers = {
            "critical": 1.75,
            "high": 1.35,
            "medium": 1.0,
            "low": 0.8,
        }
        multiplier = priority_multipliers.get(priority.lower(), 1.0)

        est_hours = round(spec["base_hours"] * multiplier, 1)
        equipment_cost = round(spec["equipment_rate_per_hr"] * est_hours, 2)
        manpower_cost = round(spec["manpower_rate_per_hr"] * est_hours, 2)
        material_cost = round(spec["material_unit_cost"] * (1.2 if multiplier > 1.2 else 1.0), 2)
        total_inr = round(equipment_cost + manpower_cost + material_cost, 2)

        return {
            "category": category.upper(),
            "priority": priority.lower(),
            "sor_reference": "PWD-TN-SOR-2025-26",
            "estimated_duration_hours": est_hours,
            "equipment_assigned": spec["equipment"],
            "manpower_crew": spec["manpower"],
            "primary_materials": spec["base_material"],
            "cost_breakdown": {
                "equipment_inr": equipment_cost,
                "manpower_inr": manpower_cost,
                "material_inr": material_cost,
                "total_estimated_inr": total_inr,
                "currency": "INR (₹)",
            },
            "financial_approval_authority": "Assistant Executive Engineer (AEE)" if total_inr > 20000 else "Junior Engineer (JE)",
        }
