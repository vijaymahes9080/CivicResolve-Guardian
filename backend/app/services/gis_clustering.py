"""
CivicResolve Guardian - Spatial GIS Clustering & Hotspot Detector
Computes Haversine geodesic distances, identifies spatial complaint density clusters (DBSCAN heuristic),
and detects infrastructure failure epicenters (e.g., ruptured water mains, transformer failures).
"""

import math
from typing import List, Dict, Any, Tuple


def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates geodesic distance in meters between two lat/lon pairs on Earth."""
    r = 6371000.0  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


class GeoIncidentCluster:
    def __init__(self, cluster_id: str, category: str):
        self.cluster_id = cluster_id
        self.category = category
        self.points: List[Dict[str, Any]] = []

    def add_point(self, point: Dict[str, Any]):
        self.points.append(point)

    @property
    def centroid(self) -> Tuple[float, float]:
        if not self.points:
            return (0.0, 0.0)
        avg_lat = sum(p["lat"] for p in self.points) / len(self.points)
        avg_lon = sum(p["lon"] for p in self.points) / len(self.points)
        return (round(avg_lat, 6), round(avg_lon, 6))

    @property
    def radius_meters(self) -> float:
        c_lat, c_lon = self.centroid
        if not self.points:
            return 0.0
        return max(haversine_distance_meters(c_lat, c_lon, p["lat"], p["lon"]) for p in self.points)

    def to_dict(self) -> Dict[str, Any]:
        c_lat, c_lon = self.centroid
        size = len(self.points)
        # Escalation multiplier: dense clusters indicate systemic infrastructure failure
        severity_escalation = "CRITICAL" if size >= 4 else "HIGH" if size >= 2 else "STANDARD"

        return {
            "cluster_id": self.cluster_id,
            "category": self.category,
            "incident_count": size,
            "centroid": {"lat": c_lat, "lon": c_lon},
            "radius_meters": round(self.radius_meters, 2),
            "severity_escalation": severity_escalation,
            "complaint_ids": [p.get("id") for p in self.points if "id" in p],
            "likely_root_cause": (
                f"Localized {self.category.lower()} failure detected across {size} reports within "
                f"{round(self.radius_meters, 1)}m radius"
            ),
        }


def detect_spatial_clusters(
    complaints: List[Dict[str, Any]],
    epsilon_meters: float = 350.0,
    min_samples: int = 2,
) -> List[Dict[str, Any]]:
    """
    Spatial clustering using a deterministic distance matrix.
    Groups complaints by category and geodesic proximity within epsilon_meters.
    """
    if not complaints:
        return []

    # Filter out entries with invalid coordinates
    valid_points = [
        c for c in complaints
        if c.get("lat") is not None and c.get("lon") is not None
    ]

    clusters: List[GeoIncidentCluster] = []
    visited = set()
    cluster_seq = 1

    for i, p1 in enumerate(valid_points):
        if i in visited:
            continue

        category = p1.get("category", "GENERAL")
        neighbors = [i]

        for j, p2 in enumerate(valid_points):
            if i == j:
                continue
            if p2.get("category", "GENERAL") == category:
                dist = haversine_distance_meters(p1["lat"], p1["lon"], p2["lat"], p2["lon"])
                if dist <= epsilon_meters:
                    neighbors.append(j)

        if len(neighbors) >= min_samples:
            cluster = GeoIncidentCluster(f"CLUSTER-{category}-{cluster_seq:03d}", category)
            cluster_seq += 1
            for idx in neighbors:
                visited.add(idx)
                cluster.add_point(valid_points[idx])
            clusters.append(cluster)

    return [c.to_dict() for c in clusters]
