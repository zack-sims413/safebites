import httpx
import asyncio
from typing import Optional, Tuple
from app.core.config import settings

class GeocodingProvider:
    """Provider for geocoding addresses to coordinates."""
    
    def __init__(self):
        self.api_key = settings.OPENCAGE_API_KEY
        self.base_url = "https://api.opencagedata.com/geocode/v1/json"
    
    async def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Geocode an address to latitude and longitude.
        
        Args:
            address: Address to geocode
            
        Returns:
            Tuple of (latitude, longitude) or None if geocoding failed
        """
        if not self.api_key:
            # Fallback to mock coordinates for development
            return self._mock_geocode(address)
        
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "q": address,
                    "key": self.api_key,
                    "limit": 1,
                    "no_annotations": 1
                }
                
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                if data["results"]:
                    result = data["results"][0]
                    lat = result["geometry"]["lat"]
                    lng = result["geometry"]["lng"]
                    return (lat, lng)
                
                return None
                
        except Exception as e:
            print(f"Geocoding failed for '{address}': {e}")
            return None
    
    def _mock_geocode(self, address: str) -> Tuple[float, float]:
        """
        Mock geocoding for development without API key.
        
        Args:
            address: Address string (not used in mock)
            
        Returns:
            Mock coordinates (Atlanta, GA)
        """
        # Return Atlanta, GA coordinates as default
        return (33.7490, -84.3880)
    
    async def reverse_geocode(self, lat: float, lng: float) -> Optional[str]:
        """
        Reverse geocode coordinates to address.
        
        Args:
            lat, lng: Coordinates
            
        Returns:
            Formatted address or None if reverse geocoding failed
        """
        if not self.api_key:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "q": f"{lat},{lng}",
                    "key": self.api_key,
                    "limit": 1,
                    "no_annotations": 1
                }
                
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                if data["results"]:
                    result = data["results"][0]
                    return result["formatted"]
                
                return None
                
        except Exception as e:
            print(f"Reverse geocoding failed for ({lat}, {lng}): {e}")
            return None

# Global instance
geocoding_provider = GeocodingProvider() 