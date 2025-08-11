import pytest
from app.scoring.wilson import (
    wilson_confidence,
    calculate_volume_bonus,
    calculate_confidence_score,
    get_confidence_breakdown
)

class TestWilsonConfidence:
    """Test Wilson lower bound confidence calculation."""
    
    def test_wilson_confidence_basic(self):
        """Test basic Wilson confidence calculation."""
        # Test with 80% positive reviews out of 10 total
        confidence = wilson_confidence(0.8, 10)
        assert 0 < confidence < 1
        assert confidence < 0.8  # Wilson lower bound should be less than observed proportion
    
    def test_wilson_confidence_small_n_penalty(self):
        """Test that small sample sizes get penalized."""
        # Same proportion, different sample sizes
        confidence_10 = wilson_confidence(0.8, 10)
        confidence_100 = wilson_confidence(0.8, 100)
        
        # Larger sample should have higher confidence
        assert confidence_100 > confidence_10
    
    def test_wilson_confidence_zero_reviews(self):
        """Test handling of zero reviews."""
        confidence = wilson_confidence(0.5, 0)
        assert confidence == 0.0
    
    def test_wilson_confidence_boundaries(self):
        """Test confidence boundaries."""
        # Test with 100% positive
        confidence_100 = wilson_confidence(1.0, 10)
        assert 0 < confidence_100 < 1
        
        # Test with 0% positive
        confidence_0 = wilson_confidence(0.0, 10)
        assert confidence_0 == 0.0

class TestVolumeBonus:
    """Test volume bonus calculation."""
    
    def test_volume_bonus_basic(self):
        """Test basic volume bonus calculation."""
        bonus_1 = calculate_volume_bonus(1)
        bonus_10 = calculate_volume_bonus(10)
        bonus_100 = calculate_volume_bonus(100)
        
        # Volume bonus should increase with more reviews
        assert bonus_10 > bonus_1
        assert bonus_100 > bonus_10
    
    def test_volume_bonus_cap(self):
        """Test that volume bonus is capped at 1.0."""
        bonus_1000 = calculate_volume_bonus(1000)
        bonus_10000 = calculate_volume_bonus(10000)
        
        assert bonus_1000 <= 1.0
        assert bonus_10000 <= 1.0
    
    def test_volume_bonus_zero_reviews(self):
        """Test volume bonus with zero reviews."""
        bonus = calculate_volume_bonus(0)
        assert bonus == 0.0

class TestConfidenceScore:
    """Test overall confidence score calculation."""
    
    def test_confidence_score_basic(self):
        """Test basic confidence score calculation."""
        # 8 positive, 2 negative out of 10 total
        confidence = calculate_confidence_score(8, 2, 10)
        
        assert 0 <= confidence <= 100
        assert isinstance(confidence, (int, float))
    
    def test_confidence_score_no_reviews(self):
        """Test confidence score with no reviews."""
        confidence = calculate_confidence_score(0, 0, 0)
        assert confidence == 0.0
    
    def test_confidence_score_all_positive(self):
        """Test confidence score with all positive reviews."""
        confidence = calculate_confidence_score(10, 0, 10)
        assert confidence > 0
    
    def test_confidence_score_all_negative(self):
        """Test confidence score with all negative reviews."""
        confidence = calculate_confidence_score(0, 10, 10)
        assert confidence == 0.0  # Should be 0 for all negative
    
    def test_confidence_score_mixed_reviews(self):
        """Test confidence score with mixed positive/negative."""
        confidence = calculate_confidence_score(5, 5, 10)
        assert 0 <= confidence <= 100
    
    def test_confidence_score_volume_effect(self):
        """Test that more reviews increase confidence."""
        # Same proportion, different volumes
        confidence_low = calculate_confidence_score(8, 2, 10)
        confidence_high = calculate_confidence_score(80, 20, 100)
        
        # Higher volume should generally have higher confidence
        assert confidence_high >= confidence_low

class TestConfidenceBreakdown:
    """Test confidence breakdown function."""
    
    def test_confidence_breakdown_basic(self):
        """Test basic confidence breakdown."""
        breakdown = get_confidence_breakdown(8, 2, 10)
        
        assert "confidence" in breakdown
        assert "wilson_lower_bound" in breakdown
        assert "volume_bonus" in breakdown
        assert "phat" in breakdown
        assert "polarized_reviews" in breakdown
        assert "total_reviews" in breakdown
        
        assert breakdown["phat"] == 0.8  # 8/(8+2)
        assert breakdown["polarized_reviews"] == 10  # 8+2
        assert breakdown["total_reviews"] == 10
    
    def test_confidence_breakdown_no_reviews(self):
        """Test confidence breakdown with no reviews."""
        breakdown = get_confidence_breakdown(0, 0, 0)
        
        assert breakdown["confidence"] == 0.0
        assert breakdown["wilson_lower_bound"] == 0.0
        assert breakdown["volume_bonus"] == 0.0
        assert breakdown["phat"] == 0.0
        assert breakdown["polarized_reviews"] == 0
        assert breakdown["total_reviews"] == 0

if __name__ == "__main__":
    pytest.main([__file__]) 