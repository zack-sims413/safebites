import re
from typing import Literal, Optional
from app.core.config import settings

SentimentType = Literal["positive", "negative", "neutral"]

class GlutenSentimentAnalyzer:
    """Analyzer for gluten safety sentiment in reviews."""
    
    def __init__(self):
        # Positive indicators for gluten safety
        self.positive_indicators = {
            "celiac safe", "celiac friendly", "gluten friendly",
            "dedicated fryer", "separate fryer", "dedicated kitchen",
            "separate kitchen", "took precautions", "no cross contamination",
            "dedicated prep area", "separate prep area", "dedicated equipment",
            "separate equipment", "gluten free menu", "gf menu",
            "allergen protocol", "allergen information", "allergen menu",
            "safe for celiac", "celiac approved", "gluten safe",
            "no issues", "no problems", "no reaction", "felt great",
            "very careful", "very accommodating", "understood my needs"
        }
        
        # Negative indicators for gluten safety
        self.negative_indicators = {
            "not safe", "got sick", "no dedicated fryer", "shared fryer",
            "shared kitchen", "cross contaminated", "cross contamination",
            "shared equipment", "not celiac safe", "not gluten friendly",
            "got glutened", "had a reaction", "made me sick",
            "didn't understand", "not careful", "no precautions",
            "shared prep area", "mixed up", "contaminated",
            "avoid if celiac", "not recommended for celiac"
        }
        
        # Negation words that can flip sentiment
        self.negation_words = {
            "no", "not", "never", "none", "nobody", "nothing", "neither",
            "nowhere", "hardly", "barely", "scarcely", "doesn't", "isn't",
            "wasn't", "shouldn't", "wouldn't", "couldn't", "won't", "can't",
            "don't", "didn't", "hasn't", "haven't", "hadn't"
        }
        
        # Compile patterns
        self.positive_patterns = [re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE) 
                                for phrase in self.positive_indicators]
        self.negative_patterns = [re.compile(r'\b' + re.escape(phrase) + r'\b', re.IGNORECASE) 
                                for phrase in self.negative_indicators]
        self.negation_pattern = re.compile(r'\b(' + '|'.join(self.negation_words) + r')\b', re.IGNORECASE)
    
    def analyze_sentiment(self, text: str) -> SentimentType:
        """
        Analyze gluten safety sentiment in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment classification: positive, negative, or neutral
        """
        if not text:
            return "neutral"
        
        text_lower = text.lower()
        
        # Count positive and negative indicators
        positive_count = sum(1 for pattern in self.positive_patterns if pattern.search(text))
        negative_count = sum(1 for pattern in self.negative_patterns if pattern.search(text))
        
        # Check for negations that might flip sentiment
        negations = len(self.negation_pattern.findall(text))
        
        # Simple rule: if more negative indicators, classify as negative
        # If more positive indicators, classify as positive
        # If equal or no indicators, classify as neutral
        if negative_count > positive_count:
            return "negative"
        elif positive_count > negative_count:
            return "positive"
        else:
            return "neutral"
    
    async def classify_with_llm(self, text: str) -> Optional[SentimentType]:
        """
        Classify sentiment using OpenAI LLM if available.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment classification or None if LLM unavailable
        """
        if not settings.OPENAI_API_KEY:
            return None
        
        try:
            import openai
            
            prompt = f"""
            Analyze the following restaurant review for gluten safety sentiment.
            Focus ONLY on gluten-related safety concerns, not general food quality.
            
            Review: "{text}"
            
            Classify as:
            - "positive" if the review indicates the restaurant is safe for gluten-free/celiac diners
            - "negative" if the review indicates the restaurant is NOT safe for gluten-free/celiac diners
            - "neutral" if the review mentions gluten but doesn't clearly indicate safety or lack thereof
            
            Respond with only: positive, negative, or neutral
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0
            )
            
            result = response.choices[0].message.content.strip().lower()
            
            if result in ["positive", "negative", "neutral"]:
                return result
            else:
                return None
                
        except Exception as e:
            # Log error and fall back to rule-based
            print(f"LLM classification failed: {e}")
            return None
    
    def get_sentiment_score(self, text: str) -> float:
        """
        Get a sentiment score between -1 and 1.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment score (-1 to 1, where -1 is very negative, 1 is very positive)
        """
        sentiment = self.analyze_sentiment(text)
        
        if sentiment == "positive":
            return 1.0
        elif sentiment == "negative":
            return -1.0
        else:
            return 0.0

# Global instance
sentiment_analyzer = GlutenSentimentAnalyzer() 