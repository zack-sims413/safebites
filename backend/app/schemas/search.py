from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SearchRequest(BaseModel):
    """Schema for search request."""
    query: str = Field(..., description="Address or location to search from")
    radiusMiles: float = Field(..., ge=0.1, le=50, description="Search radius in miles")
    cuisine: Optional[str] = Field(None, description="Optional cuisine type filter")

class Coordinates(BaseModel):
    """Schema for geographic coordinates."""
    lat: float
    lng: float

class RestaurantLinks(BaseModel):
    """Schema for restaurant links."""
    provider: str = Field(..., description="Link to provider page (Yelp)")
    maps: str = Field(..., description="Link to Google Maps")

class SearchResult(BaseModel):
    """Schema for individual search result."""
    placeId: str
    name: str
    distanceMiles: float
    confidence: int = Field(..., ge=0, le=100)
    glutenReviewCount: int
    positiveGlutenReviews: int
    negativeGlutenReviews: int
    summary: str
    address: str
    rating: Optional[float]
    userRatingsTotal: Optional[int]
    links: RestaurantLinks

class SearchResponse(BaseModel):
    """Schema for search response."""
    center: Coordinates
    rankingExplainer: str = "Confidence = Wilson lower bound on gluten-safety sentiment + volume bonus"
    results: List[SearchResult]
    totalResults: int
    searchTime: float = Field(..., description="Search time in seconds") 