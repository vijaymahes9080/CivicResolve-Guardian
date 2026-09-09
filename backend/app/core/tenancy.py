"""
CivicResolve Guardian - Multi-Municipal Corporation Tenancy Architecture
Enables multi-tenant isolation across Tamil Nadu Urban Local Bodies (ULBs)
including Greater Chennai Corporation (GCC), Coimbatore (CCMC), Madurai (MC), and Tiruchirappalli (TCC).
"""

from typing import Dict, Any, Optional


CORPORATION_TENANTS = {
    "GCC": {
        "name_en": "Greater Chennai Corporation",
        "name_ta": "பெருநகர சென்னை மாநகராட்சி",
        "hq_location": "Ripon Building, Chennai - 600003",
        "helpline": "1913",
        "total_zones": 15,
        "total_wards": 200,
        "default_lat": 13.0827,
        "default_lon": 80.2707,
        "active_departments": ["WATER_SUPPLY", "SOLID_WASTE", "ROAD_TRANSPORT", "STREET_LIGHTING", "PUBLIC_HEALTH"],
    },
    "CCMC": {
        "name_en": "Coimbatore City Municipal Corporation",
        "name_ta": "கோயம்புத்தூர் மாநகராட்சி",
        "hq_location": "Town Hall, Coimbatore - 641001",
        "helpline": "0422-2302323",
        "total_zones": 5,
        "total_wards": 100,
        "default_lat": 11.0168,
        "default_lon": 76.9558,
        "active_departments": ["WATER_SUPPLY", "SOLID_WASTE", "ROAD_TRANSPORT", "STREET_LIGHTING", "PUBLIC_HEALTH"],
    },
    "MC": {
        "name_en": "Madurai Corporation",
        "name_ta": "மதுரை மாநகராட்சி",
        "hq_location": "Aringar Anna Maligai, Madurai - 625002",
        "helpline": "0452-2530571",
        "total_zones": 5,
        "total_wards": 100,
        "default_lat": 9.9252,
        "default_lon": 78.1198,
        "active_departments": ["WATER_SUPPLY", "SOLID_WASTE", "ROAD_TRANSPORT", "STREET_LIGHTING", "PUBLIC_HEALTH"],
    },
    "TCC": {
        "name_en": "Tiruchirappalli City Corporation",
        "name_ta": "திருச்சிராப்பள்ளி மாநகராட்சி",
        "hq_location": "Bharathidasan Salai, Cantonment, Trichy - 620001",
        "helpline": "0431-2415396",
        "total_zones": 4,
        "total_wards": 65,
        "default_lat": 10.7905,
        "default_lon": 78.7047,
        "active_departments": ["WATER_SUPPLY", "SOLID_WASTE", "ROAD_TRANSPORT", "STREET_LIGHTING", "PUBLIC_HEALTH"],
    },
}


class MunicipalTenancyManager:
    """Resolves tenant context and boundaries for multi-corporation deployments."""

    @classmethod
    def get_tenant(cls, tenant_code: Optional[str] = "GCC") -> Dict[str, Any]:
        code = (tenant_code or "GCC").upper()
        tenant = CORPORATION_TENANTS.get(code, CORPORATION_TENANTS["GCC"])
        return {
            "tenant_code": code if code in CORPORATION_TENANTS else "GCC",
            **tenant,
        }

    @classmethod
    def list_available_corporations(cls) -> Dict[str, str]:
        return {code: data["name_en"] for code, data in CORPORATION_TENANTS.items()}
