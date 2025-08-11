from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class Review(Base):
    """Model for storing restaurant reviews."""
    
    __tablename__ = "reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    place_id = Column(UUID(as_uuid=True), ForeignKey("places.id"), nullable=False, index=True)
    review_id = Column(String, nullable=False, index=True)
    rating = Column(Integer)
    text = Column(Text)
    published_at = Column(DateTime(timezone=True))
    raw = Column(JSONB)  # Store complete review data from provider
    
    # Relationship
    place = relationship("Place", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review(id={self.id}, place_id={self.place_id}, rating={self.rating})>" 