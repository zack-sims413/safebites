-- SafeBites Database Initialization Script

-- Create database if it doesn't exist (this will be handled by Docker)
-- CREATE DATABASE safebites;

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create tables (these will be created by SQLAlchemy/Alembic)
-- The tables are defined in the Python models and will be created automatically

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_places_provider_id ON places(provider_id);
CREATE INDEX IF NOT EXISTS idx_places_location ON places USING GIST (ST_SetSRID(ST_MakePoint(lng, lat), 4326));
CREATE INDEX IF NOT EXISTS idx_reviews_place_id ON reviews(place_id);
CREATE INDEX IF NOT EXISTS idx_reviews_review_id ON reviews(review_id);
CREATE INDEX IF NOT EXISTS idx_gluten_signals_place_id ON gluten_signals(place_id);

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE safebites TO safebites_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO safebites_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO safebites_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO safebites_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO safebites_user; 