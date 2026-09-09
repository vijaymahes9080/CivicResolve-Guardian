"""
CivicResolve Guardian - Predictive Municipal Asset Maintenance
Forecasts catastrophic infrastructure failures (water main ruptures, grid trips, road washouts)
based on ward-level historical grievance frequency and seasonal environmental multipliers.
"""

from typing import List, Dict, Any


SEASONAL_MULTIPLIERS = {
    # Monsoon in Tamil Nadu (October - December)
    "MONSOON": {"ROAD_TRANSPORT": 2.5, "WATER_SUPPLY": 1.9, "PUBLIC_HEALTH": 2.2, "STREET_LIGHTING": 1.4, "SOLID_WASTE": 1.6},
    # Summer Heatwave (April - June)
    "SUMMER": {"STREET_LIGHTING": 1.8, "WATER_SUPPLY": 2.1, "PUBLIC_HEALTH": 1.3, "ROAD_TRANSPORT": 1.0, "SOLID_WASTE": 1.4},
    # Normal Season
    "STANDARD": {"ROAD_TRANSPORT": 1.0, "WATER_SUPPLY": 1.0, "PUBLIC_HEALTH": 1.0, "STREET_LIGHTING": 1.0, "SOLID_WASTE": 1.0},
}


class PredictiveMaintenanceForecaster:
    """Predicts infrastructure failure risks before citizen complaints surge."""

    @classmethod
    def forecast_ward_risk(
        cls,
        ward_id: str,
        recent_complaints: List[Dict[str, Any]],
        season: str = "MONSOON",
    ) -> Dict[str, Any]:
        multipliers = SEASONAL_MULTIPLIERS.get(season.upper(), SEASONAL_MULTIPLIERS["STANDARD"])

        # Count frequencies per category
        category_counts: Dict[str, int] = {}
        for c in recent_complaints:
            cat = c.get("category", "GENERAL").upper()
            category_counts[cat] = category_counts.get(cat, 0) + 1

        forecast_assessments = []
        highest_risk_score = 0.0

        for category, count in category_counts.items():
            mult = multipliers.get(category, 1.0)
            # Risk formula: base count * seasonal multiplier * recurrence factor
            raw_risk = (count * 18.5) * mult
            risk_score = min(99.0, round(raw_risk, 1))

            if risk_score > highest_risk_score:
                highest_risk_score = risk_score

            failure_prob = "CRITICAL_IMMINENT" if risk_score >= 75.0 else "ELEVATED" if risk_score >= 45.0 else "MODERATE"

            preventative_action = {
                "WATER_SUPPLY": "Dispatch ultrasonic leak detection team and inspect pressure reducer valves",
                "ROAD_TRANSPORT": "Deploy cold-mix patch crew before monsoon rain erodes road sub-base",
                "STREET_LIGHTING": "Inspect junction boxes for moisture ingress and earthing resistance",
                "SOLID_WASTE": "Increase micro-composting center clearing frequency to twice daily",
                "PUBLIC_HEALTH": "Intensify anti-larval indoor space spraying and abate application",
            }.get(category, "Conduct proactive engineering site inspection")

            forecast_assessments.append({
                "category": category,
                "recent_reports": count,
                "seasonal_multiplier": mult,
                "risk_score_pct": risk_score,
                "failure_probability": failure_prob,
                "preventative_action": preventative_action,
            })

        return {
            "ward_id": ward_id,
            "season": season.upper(),
            "overall_ward_risk_score": highest_risk_score,
            "ward_status": "RED_ALERT" if highest_risk_score >= 75.0 else "AMBER_WATCH" if highest_risk_score >= 45.0 else "GREEN_NORMAL",
            "assessments": sorted(forecast_assessments, key=lambda x: x["risk_score_pct"], reverse=True),
        }
