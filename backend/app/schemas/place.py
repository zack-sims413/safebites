from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class PlaceDetail(BaseModel):
    """Schema for detailed place information."""
    id: str
    name: str
    address: str
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    lat: float
    lng: float
    rating: Optional[float]
    userRatingsTotal: Optional[int]
    phone: Optional[str]
    website: Optional[str]
    price: Optional[str]
    categories: Optional[List[Dict[str, Any]]]
    hours: Optional[Dict[str, Any]]
    photos: Optional[List[str]]

class GlutenSnippet(BaseModel):
    """Schema for gluten-related review snippets."""
    text: str
    rating: int
    sentiment: str = Field(..., description="positive, negative, or neutral")
    publishedAt: Optional[datetime]

class PlaceDetailResponse(BaseModel):
    """Schema for place detail response."""
    place: PlaceDetail
    glutenSignal: Optional[Dict[str, Any]]
    glutenSnippets: List[GlutenSnippet]
    links: Dict[str, str] 