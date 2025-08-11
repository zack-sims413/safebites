from sqlalchemy import Column, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class GlutenSignal(Base):
    """Model for storing gluten safety analysis results."""
    
    __tablename__ = "gluten_signals"
    
    place_id = Column(UUID(as_uuid=True), ForeignKey("places.id"), primary_key=True)
    gluten_review_count = Column(Integer, default=0)
    positive_gluten_reviews = Column(Integer, default=0)
    negative_gluten_reviews = Column(Integer, default=0)
    positivity_rate = Column(Float, default=0.0)
    confidence = Column(Float, default=0.0)
    last_scored_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    place = relationship("Place", back_populates="gluten_signal")
    
    def __repr__(self):
        return f"<GlutenSignal(place_id={self.place_id}, confidence={self.confidence})>" 