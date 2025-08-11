import re
from typing import List, Set

class GlutenKeywordDetector:
    """Detector for gluten-related keywords in text."""
    
    def __init__(self):
        # Comprehensive list of gluten-related keywords
        self.gluten_keywords = {
            # Basic gluten terms
            "gluten free", "gluten-free", "gf", "celiac", "coeliac",
            "gluten allergy", "gluten intolerance", "gluten sensitive",
            
            # Cross-contamination terms
            "cross contamination", "cross-contamination", "cross contamination",
            "separate fryer", "dedicated fryer", "dedicated kitchen",
            "dedicated space", "separate kitchen", "shared equipment",
            
            # Safety indicators
            "gluten friendly", "celiac safe", "celiac friendly",
            "took precautions", "no cross contamination",
            "dedicated prep area", "separate prep area",
            
            # Negative indicators
            "not safe", "got sick", "no dedicated fryer",
            "shared fryer", "shared kitchen", "cross contaminated",
            
            # Equipment and preparation
            "dedicated equipment", "separate equipment",
            "gluten free menu", "gf menu", "allergen menu",
            "allergen information", "allergen protocol"
        }
        
        # Compile regex patterns for word boundary matching
        self.patterns = []
        for keyword in self.gluten_keywords:
            # Create case-insensitive pattern with word boundaries
            pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
            self.patterns.append(pattern)
    
    def detect_keywords(self, text: str) -> List[str]:
        """
        Detect gluten-related keywords in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of detected keywords
        """
        if not text:
            return []
        
        detected = []
        text_lower = text.lower()
        
        for pattern in self.patterns:
            if pattern.search(text):
                # Extract the actual matched keyword (preserving original case)
                matches = pattern.findall(text)
                detected.extend(matches)
        
        return list(set(detected))  # Remove duplicates
    
    def has_gluten_keywords(self, text: str) -> bool:
        """
        Check if text contains any gluten-related keywords.
        
        Args:
            text: Text to analyze
            
        Returns:
            True if gluten keywords are found, False otherwise
        """
        return len(self.detect_keywords(text)) > 0
    
    def get_keyword_count(self, text: str) -> int:
        """
        Count the number of gluten-related keywords in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Number of unique gluten keywords found
        """
        return len(self.detect_keywords(text))

# Global instance
gluten_detector = GlutenKeywordDetector() 