import httpx
import asyncio
from typing import List, Dict, Any, Optional
from app.core.config import settings

class YelpProvider:
    """Provider for Yelp Fusion API."""
    
    def __init__(self):
        self.api_key = settings.YELP_API_KEY
        self.base_url = "https://api.yelp.com/v3"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        } if self.api_key else {}
    
    async def search_businesses(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int,
        term: Optional[str] = None,
        categories: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search for businesses using Yelp Fusion API.
        
        Args:
            latitude, longitude: Search center coordinates
            radius_meters: Search radius in meters
            term: Search term (e.g., "pizza")
            categories: List of category aliases
            limit: Maximum number of results
            
        Returns:
            List of business data
        """
        if not self.api_key:
            return self._mock_search_businesses(latitude, longitude, term)
        
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "radius": radius_meters,
                    "limit": limit,
                    "sort_by": "rating"
                }
                
                if term:
                    params["term"] = term
                
                if categories:
                    params["categories"] = ",".join(categories)
                
                response = await client.get(
                    f"{self.base_url}/businesses/search",
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                
                data = response.json()
                return data.get("businesses", [])
                
        except Exception as e:
            print(f"Yelp search failed: {e}")
            return []
    
    async def get_business_details(self, business_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a business.
        
        Args:
            business_id: Yelp business ID
            
        Returns:
            Business details or None if failed
        """
        if not self.api_key:
            return self._mock_business_details(business_id)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/businesses/{business_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                
                return response.json()
                
        except Exception as e:
            print(f"Failed to get business details for {business_id}: {e}")
            return None
    
    async def get_business_reviews(
        self,
        business_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get reviews for a business.
        
        Args:
            business_id: Yelp business ID
            limit: Maximum number of reviews
            
        Returns:
            List of review data
        """
        if not self.api_key:
            return self._mock_business_reviews(business_id)
        
        try:
            async with httpx.AsyncClient() as client:
                params = {"limit": limit}
                
                response = await client.get(
                    f"{self.base_url}/businesses/{business_id}/reviews",
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                
                data = response.json()
                return data.get("reviews", [])
                
        except Exception as e:
            print(f"Failed to get reviews for {business_id}: {e}")
            return []
    
    def _mock_search_businesses(
        self,
        latitude: float,
        longitude: float,
        term: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Mock business search for development."""
        mock_businesses = [
            {
                "id": "mock-pizza-1",
                "name": "Gluten-Free Pizza Palace",
                "rating": 4.5,
                "review_count": 127,
                "price": "$$",
                "phone": "+1-555-0123",
                "display_phone": "(555) 012-3456",
                "distance": 1200,
                "coordinates": {"latitude": latitude + 0.01, "longitude": longitude + 0.01},
                "location": {
                    "address1": "123 Gluten Free St",
                    "city": "Atlanta",
                    "state": "GA",
                    "zip_code": "30301"
                },
                "categories": [{"alias": "pizza", "title": "Pizza"}],
                "url": "https://www.yelp.com/biz/mock-pizza-1"
            },
            {
                "id": "mock-italian-1",
                "name": "Celiac Safe Italian Kitchen",
                "rating": 4.8,
                "review_count": 89,
                "price": "$$$",
                "phone": "+1-555-0456",
                "display_phone": "(555) 045-6789",
                "distance": 2100,
                "coordinates": {"latitude": latitude - 0.01, "longitude": longitude - 0.01},
                "location": {
                    "address1": "456 Safe Dining Ave",
                    "city": "Atlanta",
                    "state": "GA",
                    "zip_code": "30302"
                },
                "categories": [{"alias": "italian", "title": "Italian"}],
                "url": "https://www.yelp.com/biz/mock-italian-1"
            }
        ]
        
        if term and term.lower() == "pizza":
            return [mock_businesses[0]]
        
        return mock_businesses
    
    def _mock_business_details(self, business_id: str) -> Optional[Dict[str, Any]]:
        """Mock business details for development."""
        return {
            "id": business_id,
            "name": "Mock Restaurant",
            "rating": 4.5,
            "review_count": 100,
            "price": "$$",
            "phone": "+1-555-0123",
            "display_phone": "(555) 012-3456",
            "coordinates": {"latitude": 33.7490, "longitude": -84.3880},
            "location": {
                "address1": "123 Mock St",
                "city": "Atlanta",
                "state": "GA",
                "zip_code": "30301"
            },
            "categories": [{"alias": "restaurants", "title": "Restaurants"}],
            "url": f"https://www.yelp.com/biz/{business_id}"
        }
    
    def _mock_business_reviews(self, business_id: str) -> List[Dict[str, Any]]:
        """Mock business reviews for development."""
        return [
            {
                "id": "mock-review-1",
                "rating": 5,
                "text": "Great gluten-free options! They have a dedicated fryer and the staff was very knowledgeable about celiac disease.",
                "time_created": "2023-12-01 12:00:00",
                "user": {"name": "Mock User 1"}
            },
            {
                "id": "mock-review-2",
                "rating": 4,
                "text": "Good food but limited gluten-free menu. No cross-contamination issues though.",
                "time_created": "2023-11-28 18:30:00",
                "user": {"name": "Mock User 2"}
            },
            {
                "id": "mock-review-3",
                "rating": 2,
                "text": "Not safe for celiac. They use shared equipment and I got sick.",
                "time_created": "2023-11-25 14:15:00",
                "user": {"name": "Mock User 3"}
            }
        ]

# Global instance
yelp_provider = YelpProvider() 