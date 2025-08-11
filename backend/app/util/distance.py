import math
from typing import Tuple, Optional
from app.core.config import settings

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth using Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of first point
        lat2, lon2: Latitude and longitude of second point
        
    Returns:
        Distance in miles
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of Earth in miles
    r = 3959
    
    return c * r

def calculate_distance_miles(
    lat1: float, 
    lon1: float, 
    lat2: float, 
    lon2: float,
    use_postgis: bool = True
) -> float:
    """
    Calculate distance between two points in miles.
    
    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates
        use_postgis: Whether to use PostGIS if available
        
    Returns:
        Distance in miles
    """
    if use_postgis and settings.POSTGIS_ENABLED:
        # In a real implementation, this would use PostGIS ST_Distance
        # For now, fall back to Haversine
        pass
    
    return haversine_distance(lat1, lon1, lat2, lon2)

def is_within_radius(
    center_lat: float,
    center_lon: float,
    point_lat: float,
    point_lon: float,
    radius_miles: float,
    use_postgis: bool = True
) -> bool:
    """
    Check if a point is within the specified radius of a center point.
    
    Args:
        center_lat, center_lon: Center point coordinates
        point_lat, point_lon: Point to check coordinates
        radius_miles: Radius in miles
        use_postgis: Whether to use PostGIS if available
        
    Returns:
        True if point is within radius, False otherwise
    """
    distance = calculate_distance_miles(
        center_lat, center_lon, point_lat, point_lon, use_postgis
    )
    return distance <= radius_miles

def get_bounding_box(
    center_lat: float,
    center_lon: float,
    radius_miles: float
) -> Tuple[float, float, float, float]:
    """
    Get bounding box coordinates for a given center and radius.
    
    Args:
        center_lat, center_lon: Center point coordinates
        radius_miles: Radius in miles
        
    Returns:
        Tuple of (min_lat, max_lat, min_lon, max_lon)
    """
    # Approximate degrees per mile (varies by latitude)
    # At 40 degrees latitude: 1 degree ≈ 69 miles
    degrees_per_mile = 1 / 69.0
    
    lat_delta = radius_miles * degrees_per_mile
    lon_delta = radius_miles * degrees_per_mile / math.cos(math.radians(center_lat))
    
    min_lat = center_lat - lat_delta
    max_lat = center_lat + lat_delta
    min_lon = center_lon - lon_delta
    max_lon = center_lon + lon_delta
    
    return (min_lat, max_lat, min_lon, max_lon) 