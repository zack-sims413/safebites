from sqlalchemy import Column, String, Float, Integer, DateTime, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class Place(Base):
    """Model for storing restaurant/place information."""
    
    __tablename__ = "places"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    address = Column(Text)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    rating = Column(Float)
    user_ratings_total = Column(Integer)
    last_fetched_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Additional fields for enhanced functionality
    phone = Column(String)
    website = Column(String)
    categories = Column(JSONB)  # Store Yelp categories
    price = Column(String)  # $, $$, $$$, $$$$
    hours = Column(JSONB)  # Operating hours
    photos = Column(JSONB)  # Photo URLs
    
    # Relationships
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    gluten_signal = relationship("GlutenSignal", back_populates="place", uselist=False, cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('provider_id', name='uq_place_provider_id'),
    )
    
    def __repr__(self):
        return f"<Place(id={self.id}, name='{self.name}', provider_id='{self.provider_id}')>" 