import pytest
from app.nlp.keywords import gluten_detector
from app.nlp.sentiment import sentiment_analyzer

class TestGlutenKeywordDetector:
    """Test gluten keyword detection."""
    
    def test_basic_gluten_keywords(self):
        """Test detection of basic gluten keywords."""
        text = "This restaurant has great gluten-free options"
        assert gluten_detector.has_gluten_keywords(text)
        
        keywords = gluten_detector.detect_keywords(text)
        assert "gluten-free" in [kw.lower() for kw in keywords]
    
    def test_celiac_keywords(self):
        """Test detection of celiac-related keywords."""
        text = "Safe for celiac disease patients"
        assert gluten_detector.has_gluten_keywords(text)
        
        keywords = gluten_detector.detect_keywords(text)
        assert "celiac" in [kw.lower() for kw in keywords]
    
    def test_cross_contamination_keywords(self):
        """Test detection of cross-contamination keywords."""
        text = "They use separate fryers to avoid cross contamination"
        assert gluten_detector.has_gluten_keywords(text)
        
        keywords = gluten_detector.detect_keywords(text)
        assert "cross contamination" in [kw.lower() for kw in keywords]
        assert "separate fryer" in [kw.lower() for kw in keywords]
    
    def test_dedicated_equipment_keywords(self):
        """Test detection of dedicated equipment keywords."""
        text = "They have dedicated kitchen equipment for gluten-free cooking"
        assert gluten_detector.has_gluten_keywords(text)
        
        keywords = gluten_detector.detect_keywords(text)
        assert "dedicated kitchen" in [kw.lower() for kw in keywords]
    
    def test_no_gluten_keywords(self):
        """Test text without gluten keywords."""
        text = "This restaurant has great food and friendly service"
        assert not gluten_detector.has_gluten_keywords(text)
        
        keywords = gluten_detector.detect_keywords(text)
        assert len(keywords) == 0
    
    def test_case_insensitive_detection(self):
        """Test case-insensitive keyword detection."""
        text = "GLUTEN FREE options available"
        assert gluten_detector.has_gluten_keywords(text)
        
        text = "Celiac Safe Restaurant"
        assert gluten_detector.has_gluten_keywords(text)
    
    def test_word_boundary_detection(self):
        """Test that keywords are detected with word boundaries."""
        text = "The glutenfree pizza was good"  # No space
        assert not gluten_detector.has_gluten_keywords(text)
        
        text = "The gluten-free pizza was good"  # With space
        assert gluten_detector.has_gluten_keywords(text)
    
    def test_keyword_count(self):
        """Test keyword counting."""
        text = "Gluten-free options with dedicated fryer and celiac safe menu"
        count = gluten_detector.get_keyword_count(text)
        assert count >= 3  # Should detect multiple keywords
    
    def test_empty_text(self):
        """Test handling of empty text."""
        assert not gluten_detector.has_gluten_keywords("")
        assert len(gluten_detector.detect_keywords("")) == 0
        assert gluten_detector.get_keyword_count("") == 0

class TestGlutenSentimentAnalyzer:
    """Test gluten safety sentiment analysis."""
    
    def test_positive_sentiment(self):
        """Test positive gluten safety sentiment."""
        text = "This restaurant is celiac safe with dedicated fryer"
        sentiment = sentiment_analyzer.analyze_sentiment(text)
        assert sentiment == "positive"
    
    def test_negative_sentiment(self):
        """Test negative gluten safety sentiment."""
        text = "Not safe for celiac, they use shared equipment"
        sentiment = sentiment_analyzer.analyze_sentiment(text)
        assert sentiment == "negative"
    
    def test_neutral_sentiment(self):
        """Test neutral sentiment."""
        text = "They have some gluten-free options"
        sentiment = sentiment_analyzer.analyze_sentiment(text)
        assert sentiment == "neutral"
    
    def test_mixed_sentiment(self):
        """Test mixed positive and negative indicators."""
        text = "They have dedicated fryer but also shared kitchen"
        sentiment = sentiment_analyzer.analyze_sentiment(text)
        # Should be neutral or based on which indicators are stronger
        assert sentiment in ["positive", "negative", "neutral"]
    
    def test_negation_handling(self):
        """Test handling of negations."""
        text = "They do not have dedicated fryer"
        sentiment = sentiment_analyzer.analyze_sentiment(text)
        assert sentiment == "negative"
    
    def test_safety_indicators(self):
        """Test various safety indicators."""
        positive_texts = [
            "Celiac safe restaurant",
            "Dedicated fryer for gluten-free items",
            "Separate kitchen area",
            "Took proper precautions",
            "No cross-contamination issues"
        ]
        
        for text in positive_texts:
            sentiment = sentiment_analyzer.analyze_sentiment(text)
            assert sentiment == "positive"
    
    def test_unsafety_indicators(self):
        """Test various unsafety indicators."""
        negative_texts = [
            "Not safe for celiac",
            "Shared fryer used",
            "Cross-contamination occurred",
            "Got sick after eating here",
            "No dedicated equipment"
        ]
        
        for text in negative_texts:
            sentiment = sentiment_analyzer.analyze_sentiment(text)
            assert sentiment == "negative"
    
    def test_empty_text_sentiment(self):
        """Test handling of empty text."""
        sentiment = sentiment_analyzer.analyze_sentiment("")
        assert sentiment == "neutral"
    
    def test_sentiment_score(self):
        """Test sentiment score calculation."""
        positive_score = sentiment_analyzer.get_sentiment_score("Celiac safe restaurant")
        assert positive_score == 1.0
        
        negative_score = sentiment_analyzer.get_sentiment_score("Not safe for celiac")
        assert negative_score == -1.0
        
        neutral_score = sentiment_analyzer.get_sentiment_score("Some gluten-free options")
        assert neutral_score == 0.0

class TestIntegration:
    """Test integration between keyword detection and sentiment analysis."""
    
    def test_gluten_review_analysis(self):
        """Test complete analysis of a gluten-related review."""
        review = "Great gluten-free pizza! They have a dedicated fryer and the staff was very knowledgeable about celiac disease."
        
        # Should detect keywords
        assert gluten_detector.has_gluten_keywords(review)
        
        # Should be positive sentiment
        sentiment = sentiment_analyzer.analyze_sentiment(review)
        assert sentiment == "positive"
        
        # Should have positive sentiment score
        score = sentiment_analyzer.get_sentiment_score(review)
        assert score == 1.0
    
    def test_negative_gluten_review(self):
        """Test analysis of negative gluten review."""
        review = "Not safe for celiac. They use shared equipment and I got sick after eating here."
        
        # Should detect keywords
        assert gluten_detector.has_gluten_keywords(review)
        
        # Should be negative sentiment
        sentiment = sentiment_analyzer.analyze_sentiment(review)
        assert sentiment == "negative"
        
        # Should have negative sentiment score
        score = sentiment_analyzer.get_sentiment_score(review)
        assert score == -1.0

if __name__ == "__main__":
    pytest.main([__file__]) 