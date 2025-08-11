# SafeBites - Gluten-Friendly Restaurant Finder

A web application that helps users find restaurants that can safely accommodate gluten allergies, celiac disease, and gluten intolerances.

## 🚨 Safety Disclaimer

**Important for Celiac Users**: While SafeBites analyzes reviews and ratings to identify potentially gluten-safe restaurants, we cannot guarantee 100% safety. Always:
- Contact restaurants directly to confirm their gluten-free protocols
- Ask about cross-contamination procedures
- Verify dedicated cooking spaces and equipment
- Consult with your healthcare provider about your specific dietary needs

This tool is for informational purposes only and should not replace proper medical advice or direct communication with restaurants.

## 🏗️ Project Structure

```
safebites/
├── frontend/          # Next.js 14 + TypeScript + Tailwind
├── backend/           # FastAPI + SQLAlchemy + PostgreSQL
├── docker/            # Docker configuration
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Environment Setup

#### Backend Environment Variables
Create `backend/.env`:
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/safebites
POSTGIS_ENABLED=true

# API Keys
YELP_API_KEY=your_yelp_fusion_api_key
OPENCAGE_API_KEY=your_opencage_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional

# Cache Settings
CACHE_TTL_SECONDS=86400  # 24 hours

# App Settings
DEBUG=true
LOG_LEVEL=INFO
```

#### Frontend Environment Variables
Create `frontend/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=SafeBites
```

### Running with Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/zack-sims413/safebites.git
cd safebites
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Running Locally

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔧 Mock Mode

For development without API keys, use mock mode:
- Add `?mock=1` to any search request
- Returns canned results for testing

## 📊 API Endpoints

### POST /api/search
Search for gluten-friendly restaurants.

**Request Body:**
```json
{
  "query": "Atlanta, GA",
  "radiusMiles": 10,
  "cuisine": "pizza"
}
```

**Response:**
```json
{
  "center": {"lat": 33.749, "lng": -84.388},
  "rankingExplainer": "Confidence = Wilson lower bound on gluten-safety sentiment + volume bonus",
  "results": [
    {
      "placeId": "...",
      "name": "...",
      "distanceMiles": 1.2,
      "confidence": 83,
      "glutenReviewCount": 17,
      "positiveGlutenReviews": 12,
      "negativeGlutenReviews": 3,
      "summary": "...",
      "address": "...",
      "rating": 4.4,
      "userRatingsTotal": 287,
      "links": {
        "provider": "...",
        "maps": "..."
      }
    }
  ]
}
```

### GET /api/places/{id}
Get detailed information about a specific restaurant.

## 🎯 Features

- **Geolocation Search**: Find restaurants within specified radius
- **Cuisine Filtering**: Filter by cuisine type (optional)
- **Gluten Safety Analysis**: AI-powered review analysis for gluten safety indicators
- **Confidence Scoring**: Wilson lower bound scoring with volume bonus
- **Distance Calculation**: Accurate distance calculations using PostGIS or Haversine
- **Caching**: Efficient caching to minimize API calls
- **Mock Mode**: Development mode with canned data

## 🔍 How It Works

1. **Geocoding**: Convert user address to coordinates
2. **Provider Search**: Query Yelp Fusion API for restaurants
3. **Review Analysis**: Analyze reviews for gluten-related keywords and sentiment
4. **Scoring**: Calculate confidence scores using Wilson lower bound
5. **Ranking**: Sort by confidence (descending) and distance (ascending)
6. **Caching**: Store results to minimize API usage

## 📝 Terms of Service

- **No Scraping**: This application uses only official APIs (Yelp Fusion, OpenCage)
- **Rate Limiting**: Respects all API rate limits with exponential backoff
- **Data Privacy**: User data is not stored or shared
- **API Usage**: Users are responsible for their own API key usage and costs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the test files for usage examples
3. Open an issue on GitHub

## 🔄 Updates

- **v1.0.0**: Initial release with core functionality
- Basic gluten safety detection
- Wilson confidence scoring
- Distance-based search
- Cuisine filtering
