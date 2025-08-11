import math
from typing import Tuple

def wilson_confidence(phat: float, n: int, z: float = 1.96) -> float:
    """
    Calculate Wilson lower bound confidence score.
    
    Args:
        phat: Observed proportion of positive reviews
        n: Total number of reviews
        z: Z-score for confidence level (default 1.96 for 95% confidence)
        
    Returns:
        Wilson lower bound confidence score
    """
    if n <= 0:
        return 0.0
    
    z2 = z * z
    denom = 1 + z2 / n
    center = phat + z2 / (2 * n)
    margin = z * math.sqrt((phat * (1 - phat) + z2 / (4 * n)) / n)
    lb = (center - margin) / denom
    
    return max(0.0, min(1.0, lb))

def calculate_volume_bonus(n: int) -> float:
    """
    Calculate volume bonus based on number of reviews.
    
    Args:
        n: Number of reviews
        
    Returns:
        Volume bonus score (0 to 1)
    """
    if n <= 0:
        return 0.0
    
    # Log-scaled volume bonus, capped at 1.0
    volume_bonus = min(1.0, max(0.0, math.log10(n + 1)) / 2.0)
    return volume_bonus

def calculate_confidence_score(
    positive_reviews: int, 
    negative_reviews: int, 
    total_reviews: int,
    z: float = 1.96
) -> float:
    """
    Calculate overall confidence score using Wilson lower bound + volume bonus.
    
    Args:
        positive_reviews: Number of positive gluten reviews
        negative_reviews: Number of negative gluten reviews
        total_reviews: Total number of gluten-related reviews
        z: Z-score for confidence level
        
    Returns:
        Confidence score from 0 to 100
    """
    if total_reviews <= 0:
        return 0.0
    
    # Calculate proportion of positive reviews (only from polarized reviews)
    polarized_reviews = positive_reviews + negative_reviews
    if polarized_reviews <= 0:
        return 0.0
    
    phat = positive_reviews / polarized_reviews
    
    # Calculate Wilson lower bound
    wilson_lb = wilson_confidence(phat, polarized_reviews, z)
    
    # Calculate volume bonus
    volume_bonus = calculate_volume_bonus(total_reviews)
    
    # Combine scores: 70% Wilson + 30% volume bonus
    raw_score = 0.7 * wilson_lb + 0.3 * volume_bonus
    
    # Convert to 0-100 scale and round
    confidence = round(100 * max(0.0, min(1.0, raw_score)))
    
    return confidence

def get_confidence_breakdown(
    positive_reviews: int, 
    negative_reviews: int, 
    total_reviews: int,
    z: float = 1.96
) -> dict:
    """
    Get detailed breakdown of confidence calculation.
    
    Args:
        positive_reviews: Number of positive gluten reviews
        negative_reviews: Number of negative gluten reviews
        total_reviews: Total number of gluten-related reviews
        z: Z-score for confidence level
        
    Returns:
        Dictionary with confidence breakdown
    """
    polarized_reviews = positive_reviews + negative_reviews
    
    if polarized_reviews <= 0:
        return {
            "confidence": 0.0,
            "wilson_lower_bound": 0.0,
            "volume_bonus": 0.0,
            "phat": 0.0,
            "polarized_reviews": 0,
            "total_reviews": total_reviews
        }
    
    phat = positive_reviews / polarized_reviews
    wilson_lb = wilson_confidence(phat, polarized_reviews, z)
    volume_bonus = calculate_volume_bonus(total_reviews)
    confidence = calculate_confidence_score(positive_reviews, negative_reviews, total_reviews, z)
    
    return {
        "confidence": confidence,
        "wilson_lower_bound": wilson_lb,
        "volume_bonus": volume_bonus,
        "phat": phat,
        "polarized_reviews": polarized_reviews,
        "total_reviews": total_reviews
    } 