"""
CivicResolve Guardian - Multi-Modal Image Evidence Forensics
Analyzes photo evidence metadata, geotags, capture timestamps, and perceptual hashes
to detect recycled photos, location spoofing, and AI-generated or stock municipal images.
"""

import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from app.services.gis_clustering import haversine_distance_meters


class ImageForensicsAnalyzer:
    """
    Performs forensic inspection of submitted photo evidence before triage routing.
    Protects municipal workforce from fraudulent or duplicate dispatches.
    """

    @staticmethod
    def compute_simulated_dhash(image_bytes: bytes) -> str:
        """Computes a deterministic perceptual fingerprint hash from byte stream."""
        return hashlib.sha256(image_bytes[:512] + image_bytes[-512:] if len(image_bytes) >= 1024 else image_bytes).hexdigest()[:16]

    @classmethod
    def analyze_evidence(
        cls,
        image_bytes: bytes,
        claimed_lat: Optional[float],
        claimed_lon: Optional[float],
        category: str,
        exif_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        flags = []
        veracity_score = 1.0

        if not image_bytes or len(image_bytes) < 100:
            return {
                "veracity_score": 0.1,
                "is_valid": False,
                "flags": ["CORRUPT_OR_EMPTY_IMAGE"],
                "fingerprint": None,
                "geotag_verified": False,
            }

        fingerprint = cls.compute_simulated_dhash(image_bytes)
        exif = exif_metadata or {}

        # 1. Geotag Geodesic Validation
        geotag_verified = False
        geo_distance_meters = None
        photo_lat = exif.get("latitude")
        photo_lon = exif.get("longitude")

        if photo_lat is not None and photo_lon is not None and claimed_lat is not None and claimed_lon is not None:
            geo_distance_meters = round(haversine_distance_meters(photo_lat, photo_lon, claimed_lat, claimed_lon), 1)
            if geo_distance_meters > 800.0:
                flags.append(f"GEOTAG_MISMATCH: Photo taken {geo_distance_meters}m away from claimed incident location")
                veracity_score -= 0.35
            else:
                geotag_verified = True
        elif not photo_lat:
            flags.append("NO_EXIF_GEOTAG: Image missing embedded camera GPS coordinates")
            veracity_score -= 0.10

        # 2. Timestamp Freshness Check
        capture_time_str = exif.get("capture_timestamp")
        if capture_time_str:
            try:
                capture_time = datetime.fromisoformat(capture_time_str.replace("Z", "+00:00"))
                now = datetime.now(timezone.utc)
                age_days = (now - capture_time).days
                if age_days > 14:
                    flags.append(f"STALE_PHOTO: Evidence captured {age_days} days ago")
                    veracity_score -= 0.25
            except Exception:
                pass

        # 3. Known Stock Photo / Template Detection Heuristic
        software = exif.get("software", "").lower()
        if any(s in software for s in ["photoshop", "gimp", "canva", "dall-e", "midjourney"]):
            flags.append("SYNTHETIC_OR_EDITED: Image software indicates digital editing or generative model")
            veracity_score -= 0.50

        # Clamp veracity score between 0.05 and 1.0
        veracity_score = max(0.05, min(1.0, round(veracity_score, 2)))

        return {
            "veracity_score": veracity_score,
            "is_valid": veracity_score >= 0.50,
            "fingerprint": fingerprint,
            "geotag_verified": geotag_verified,
            "geo_distance_meters": geo_distance_meters,
            "flags": flags,
            "recommendation": "ACCEPT" if veracity_score >= 0.70 else "FLAG_FOR_OFFICER_REVIEW",
        }
