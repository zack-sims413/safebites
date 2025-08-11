import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestSearchAPI:
    """Test the search API endpoint."""
    
    def test_search_with_mock_data(self):
        """Test search endpoint with mock data."""
        search_data = {
            "query": "Atlanta, GA",
            "radiusMiles": 10,
            "cuisine": "pizza"
        }
        
        response = client.post("/api/search?mock=1", json=search_data)
        
        assert response.status_code == 200
        
        data = response.json()
        assert "results" in data
        assert "center" in data
        assert "totalResults" in data
        assert "searchTime" in data
        
        # Should have results with mock data
        assert len(data["results"]) > 0
        
        # Check result structure
        result = data["results"][0]
        assert "placeId" in result
        assert "name" in result
        assert "distanceMiles" in result
        assert "confidence" in result
        assert "glutenReviewCount" in result
        assert "positiveGlutenReviews" in result
        assert "negativeGlutenReviews" in result
        assert "summary" in result
        assert "address" in result
        assert "links" in result
    
    def test_search_without_cuisine(self):
        """Test search endpoint without cuisine filter."""
        search_data = {
            "query": "Atlanta, GA",
            "radiusMiles": 10
        }
        
        response = client.post("/api/search?mock=1", json=search_data)
        
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["results"]) > 0
    
    def test_search_invalid_location(self):
        """Test search with invalid location."""
        search_data = {
            "query": "",
            "radiusMiles": 10
        }
        
        response = client.post("/api/search", json=search_data)
        
        # Should return 400 for empty query
        assert response.status_code == 400
    
    def test_search_invalid_radius(self):
        """Test search with invalid radius."""
        search_data = {
            "query": "Atlanta, GA",
            "radiusMiles": 100  # Too large
        }
        
        response = client.post("/api/search", json=search_data)
        
        # Should return 422 for validation error
        assert response.status_code == 422

class TestPlaceDetailsAPI:
    """Test the place details API endpoint."""
    
    def test_place_details_with_mock_data(self):
        """Test place details endpoint with mock data."""
        place_id = "mock-pizza-1"
        
        response = client.get(f"/api/places/{place_id}?mock=1")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "place" in data
        assert "glutenSignal" in data
        assert "glutenSnippets" in data
        assert "links" in data
        
        # Check place structure
        place = data["place"]
        assert "id" in place
        assert "name" in place
        assert "address" in place
        assert "lat" in place
        assert "lng" in place
    
    def test_place_details_not_found(self):
        """Test place details with non-existent place."""
        place_id = "non-existent-place"
        
        response = client.get(f"/api/places/{place_id}?mock=1")
        
        # Should return 404 for non-existent place
        assert response.status_code == 404

class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "safebites-api"
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data

if __name__ == "__main__":
    pytest.main([__file__]) 