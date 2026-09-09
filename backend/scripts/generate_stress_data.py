"""
CivicResolve Guardian - Municipal High-Volume Stress Data Generator
Generates realistic high-density synthetic complaint records across Tamil Nadu municipal wards
for concurrency stress-testing, database scaling, and machine learning triage benchmarking.
"""

import random
from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta


TAMIL_TEMPLATES = [
    "எங்கள் பகுதியில் {street} தெருவில் குடிநீர் குழாய் உடைந்து தண்ணீர் வீணாகிறது.",
    "{street} பிரதான சாலையில் பெரிய பள்ளம் ஏற்பட்டு வாகன ஓட்டிகள் விபத்துக்குள்ளாகின்றனர்.",
    "{street} சந்திப்பில் உள்ள குப்பை தொட்டி நிரம்பி வழிகிறது, துர்நாற்றம் வீசுகிறது.",
    "{street} தெருவிளக்கு பல நாட்களாக எரியவில்லை. இரவில் மக்கள் செல்ல அச்சப்படுகின்றனர்.",
]

ENGLISH_TEMPLATES = [
    "Severe drinking water leakage flooding {street}, please repair urgent pipe burst.",
    "Dangerous crater pothole on {street} causing traffic congestion and accidents.",
    "Garbage bin overflowing for three days near {street}, stray cattle nuisance.",
    "Street light pole flickering and tripping power breaker at {street}.",
]

STREETS = [
    "Anna Salai", "Poonamallee High Road", "Gandhi Irwin Road", "100 Feet Road",
    "Jawaharlal Nehru Road", "Arcot Road", "Sardar Patel Road", "Velachery Main Road",
    "G.S.T Road", "Old Mahabalipuram Road (OMR)", "East Coast Road (ECR)"
]

CATEGORIES = ["WATER_SUPPLY", "ROAD_TRANSPORT", "SOLID_WASTE", "STREET_LIGHTING", "PUBLIC_HEALTH"]
PRIORITIES = ["critical", "high", "medium", "low"]


def generate_synthetic_record(record_id: int) -> Dict[str, Any]:
    street = random.choice(STREETS)
    category = random.choice(CATEGORIES)
    priority = random.choice(PRIORITIES)
    is_tamil = random.random() > 0.5

    # Coordinates around Chennai bounding box (lat ~ 12.95 - 13.15, lon ~ 80.15 - 80.30)
    lat = round(random.uniform(12.95, 13.15), 6)
    lon = round(random.uniform(80.15, 80.30), 6)
    ward_num = random.randint(1, 200)

    # Random simulated submission within past 14 days
    days_ago = random.randint(0, 14)
    timestamp = (datetime.now(timezone.utc) - timedelta(days=days_ago, minutes=random.randint(0, 1400))).isoformat()

    title = random.choice(TAMIL_TEMPLATES if is_tamil else ENGLISH_TEMPLATES).format(street=street)

    return {
        "id": f"STRESS-{record_id:06d}",
        "ward_id": f"WARD-{ward_num:03d}",
        "category": category,
        "priority": priority,
        "title": title,
        "language": "ta" if is_tamil else "en",
        "latitude": lat,
        "longitude": lon,
        "created_at": timestamp,
        "status": random.choice(["submitted", "triage_recommended", "officer_approved", "resolved"]),
    }


def generate_batch(count: int = 100) -> List[Dict[str, Any]]:
    return [generate_synthetic_record(i + 1) for i in range(count)]


if __name__ == "__main__":
    records = generate_batch(50)
    print(f"Generated {len(records)} stress test records successfully. Sample:")
    print(records[0])
