from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import time

from app.db.base import get_db
from app.schemas.search import SearchRequest, SearchResponse, Coordinates, SearchResult, RestaurantLinks
from app.schemas.place import PlaceDetailResponse, PlaceDetail, GlutenSnippet
from app.providers.geocode import geocoding_provider
from app.providers.yelp import yelp_provider
from app.nlp.keywords import gluten_detector
from app.nlp.sentiment import sentiment_analyzer
from app.scoring.wilson import calculate_confidence_score
from app.util.distance import calculate_distance_miles
from app.util.cuisine import cuisine_mapper
from app.core.config import settings

router = APIRouter()

@router.post("/search", response_model=SearchResponse)
async def search_restaurants(
    request: SearchRequest,
    mock: bool = Query(False, description="Use mock data for testing"),
    db: AsyncSession = Depends(get_db)
):
    """
    Search for gluten-friendly restaurants.
    
    Args:
        request: Search parameters
        mock: Use mock data (for development)
        db: Database session
        
    Returns:
        Search results with gluten safety analysis
    """
    start_time = time.time()
    
    try:
        # Geocode the search location
        coords = await geocoding_provider.geocode_address(request.query)
        if not coords:
            raise HTTPException(status_code=400, detail="Could not geocode the provided address")
        
        lat, lng = coords
        center = Coordinates(lat=lat, lng=lng)
        
        # Convert radius from miles to meters for Yelp API
        radius_meters = int(request.radiusMiles * 1609.34)
        
        # Get cuisine search terms
        search_term = None
        if request.cuisine:
            search_term = cuisine_mapper.get_primary_search_term(request.cuisine)
        
        # Search for businesses
        if mock or settings.MOCK_MODE_ENABLED:
            businesses = yelp_provider._mock_search_businesses(lat, lng, search_term)
        else:
            businesses = await yelp_provider.search_businesses(
                latitude=lat,
                longitude=lng,
                radius_meters=radius_meters,
                term=search_term,
                limit=50
            )
        
        results = []
        
        for business in businesses:
            # Calculate distance
            distance_miles = calculate_distance_miles(
                lat, lng,
                business["coordinates"]["latitude"],
                business["coordinates"]["longitude"]
            )
            
            # Skip if outside radius
            if distance_miles > request.radiusMiles:
                continue
            
            # Get reviews for gluten analysis
            if mock or settings.MOCK_MODE_ENABLED:
                reviews = yelp_provider._mock_business_reviews(business["id"])
            else:
                reviews = await yelp_provider.get_business_reviews(business["id"])
            
            # Analyze reviews for gluten safety
            gluten_reviews = []
            positive_count = 0
            negative_count = 0
            
            for review in reviews:
                review_text = review.get("text", "")
                
                # Check if review contains gluten-related keywords
                if gluten_detector.has_gluten_keywords(review_text):
                    gluten_reviews.append(review)
                    
                    # Analyze sentiment
                    sentiment = sentiment_analyzer.analyze_sentiment(review_text)
                    if sentiment == "positive":
                        positive_count += 1
                    elif sentiment == "negative":
                        negative_count += 1
            
            # Calculate confidence score
            total_gluten_reviews = len(gluten_reviews)
            confidence = calculate_confidence_score(
                positive_count, negative_count, total_gluten_reviews
            )
            
            # Generate summary from gluten reviews
            summary = _generate_gluten_summary(gluten_reviews)
            
            # Create links
            links = RestaurantLinks(
                provider=business.get("url", ""),
                maps=f"https://maps.google.com/?q={business['coordinates']['latitude']},{business['coordinates']['longitude']}"
            )
            
            # Create result
            result = SearchResult(
                placeId=business["id"],
                name=business["name"],
                distanceMiles=round(distance_miles, 1),
                confidence=int(confidence),
                glutenReviewCount=total_gluten_reviews,
                positiveGlutenReviews=positive_count,
                negativeGlutenReviews=negative_count,
                summary=summary,
                address=business["location"].get("address1", ""),
                rating=business.get("rating"),
                userRatingsTotal=business.get("review_count"),
                links=links
            )
            
            results.append(result)
        
        # Sort by confidence (descending) then distance (ascending)
        results.sort(key=lambda x: (-x.confidence, x.distanceMiles))
        
        # Apply cuisine filter if specified
        if request.cuisine:
            filtered_results = []
            for result in results:
                # Get business details to check categories
                if mock or settings.MOCK_MODE_ENABLED:
                    business_details = yelp_provider._mock_business_details(result.placeId)
                else:
                    business_details = await yelp_provider.get_business_details(result.placeId)
                
                if business_details:
                    categories = [cat["alias"] for cat in business_details.get("categories", [])]
                    if cuisine_mapper.is_cuisine_match(
                        result.name, categories, request.cuisine
                    ):
                        filtered_results.append(result)
            
            # If no strong matches, return top results with a flag
            if not filtered_results and results:
                filtered_results = results[:5]  # Return top 5 anyway
            
            results = filtered_results
        
        search_time = time.time() - start_time
        
        return SearchResponse(
            center=center,
            rankingExplainer="Confidence = Wilson lower bound on gluten-safety sentiment + volume bonus",
            results=results,
            totalResults=len(results),
            searchTime=round(search_time, 2)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/places/{place_id}", response_model=PlaceDetailResponse)
async def get_place_details(
    place_id: str,
    mock: bool = Query(False, description="Use mock data for testing"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed information about a specific restaurant.
    
    Args:
        place_id: Yelp business ID
        mock: Use mock data (for development)
        db: Database session
        
    Returns:
        Place details with gluten analysis
    """
    try:
        # Get business details
        if mock or settings.MOCK_MODE_ENABLED:
            business = yelp_provider._mock_business_details(place_id)
        else:
            business = await yelp_provider.get_business_details(place_id)
        
        if not business:
            raise HTTPException(status_code=404, detail="Place not found")
        
        # Get reviews
        if mock or settings.MOCK_MODE_ENABLED:
            reviews = yelp_provider._mock_business_reviews(place_id)
        else:
            reviews = await yelp_provider.get_business_reviews(place_id)
        
        # Analyze gluten-related reviews
        gluten_snippets = []
        positive_count = 0
        negative_count = 0
        total_gluten_reviews = 0
        
        for review in reviews:
            review_text = review.get("text", "")
            
            if gluten_detector.has_gluten_keywords(review_text):
                total_gluten_reviews += 1
                sentiment = sentiment_analyzer.analyze_sentiment(review_text)
                
                if sentiment == "positive":
                    positive_count += 1
                elif sentiment == "negative":
                    negative_count += 1
                
                # Create snippet (truncate if too long)
                snippet_text = review_text[:200] + "..." if len(review_text) > 200 else review_text
                
                snippet = GlutenSnippet(
                    text=snippet_text,
                    rating=review.get("rating", 0),
                    sentiment=sentiment,
                    publishedAt=None  # Could parse from review data if available
                )
                gluten_snippets.append(snippet)
        
        # Calculate confidence
        confidence = calculate_confidence_score(
            positive_count, negative_count, total_gluten_reviews
        )
        
        # Create gluten signal data
        gluten_signal = {
            "confidence": int(confidence),
            "glutenReviewCount": total_gluten_reviews,
            "positiveGlutenReviews": positive_count,
            "negativeGlutenReviews": negative_count,
            "positivityRate": positive_count / max(1, positive_count + negative_count)
        }
        
        # Create place detail
        place = PlaceDetail(
            id=business["id"],
            name=business["name"],
            address=business["location"].get("address1", ""),
            city=business["location"].get("city"),
            state=business["location"].get("state"),
            country=business["location"].get("country"),
            lat=business["coordinates"]["latitude"],
            lng=business["coordinates"]["longitude"],
            rating=business.get("rating"),
            userRatingsTotal=business.get("review_count"),
            phone=business.get("phone"),
            website=business.get("url"),
            price=business.get("price"),
            categories=business.get("categories"),
            hours=None,  # Could be added if available
            photos=None   # Could be added if available
        )
        
        # Create links
        links = {
            "provider": business.get("url", ""),
            "maps": f"https://maps.google.com/?q={business['coordinates']['latitude']},{business['coordinates']['longitude']}"
        }
        
        return PlaceDetailResponse(
            place=place,
            glutenSignal=gluten_signal,
            glutenSnippets=gluten_snippets[:10],  # Limit to top 10 snippets
            links=links
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get place details: {str(e)}")

def _generate_gluten_summary(reviews: list) -> str:
    """Generate a summary of gluten-related reviews."""
    if not reviews:
        return "No gluten-related reviews found."
    
    positive_count = 0
    negative_count = 0
    
    for review in reviews:
        sentiment = sentiment_analyzer.analyze_sentiment(review.get("text", ""))
        if sentiment == "positive":
            positive_count += 1
        elif sentiment == "negative":
            negative_count += 1
    
    total = len(reviews)
    
    if positive_count > negative_count:
        return f"Mostly positive gluten reviews ({positive_count}/{total} positive)"
    elif negative_count > positive_count:
        return f"Mostly negative gluten reviews ({negative_count}/{total} negative)"
    else:
        return f"Mixed gluten reviews ({positive_count} positive, {negative_count} negative out of {total})" 