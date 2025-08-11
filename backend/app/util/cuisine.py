from typing import Dict, List, Optional, Tuple

class CuisineMapper:
    """Maps cuisine types to Yelp search terms and categories."""
    
    def __init__(self):
        # Mapping of common cuisine types to Yelp search terms and categories
        self.cuisine_mapping = {
            # Italian
            "italian": {
                "terms": ["italian", "pizza", "pasta"],
                "categories": ["italian", "pizza", "pasta"]
            },
            "pizza": {
                "terms": ["pizza", "italian"],
                "categories": ["pizza", "italian"]
            },
            "pasta": {
                "terms": ["pasta", "italian"],
                "categories": ["pasta", "italian"]
            },
            
            # Asian
            "chinese": {
                "terms": ["chinese"],
                "categories": ["chinese"]
            },
            "japanese": {
                "terms": ["japanese", "sushi"],
                "categories": ["japanese", "sushi"]
            },
            "sushi": {
                "terms": ["sushi", "japanese"],
                "categories": ["sushi", "japanese"]
            },
            "thai": {
                "terms": ["thai"],
                "categories": ["thai"]
            },
            "vietnamese": {
                "terms": ["vietnamese"],
                "categories": ["vietnamese"]
            },
            "korean": {
                "terms": ["korean"],
                "categories": ["korean"]
            },
            "indian": {
                "terms": ["indian"],
                "categories": ["indian"]
            },
            
            # American
            "american": {
                "terms": ["american", "burgers"],
                "categories": ["american", "burgers"]
            },
            "burgers": {
                "terms": ["burgers", "american"],
                "categories": ["burgers", "american"]
            },
            "bbq": {
                "terms": ["bbq", "barbecue"],
                "categories": ["bbq", "barbecue"]
            },
            
            # Mexican
            "mexican": {
                "terms": ["mexican", "tacos"],
                "categories": ["mexican", "tacos"]
            },
            "tacos": {
                "terms": ["tacos", "mexican"],
                "categories": ["tacos", "mexican"]
            },
            
            # Mediterranean
            "mediterranean": {
                "terms": ["mediterranean", "greek"],
                "categories": ["mediterranean", "greek"]
            },
            "greek": {
                "terms": ["greek", "mediterranean"],
                "categories": ["greek", "mediterranean"]
            },
            
            # Other
            "seafood": {
                "terms": ["seafood", "fish"],
                "categories": ["seafood"]
            },
            "steakhouse": {
                "terms": ["steakhouse", "steak"],
                "categories": ["steakhouse"]
            },
            "vegetarian": {
                "terms": ["vegetarian", "vegan"],
                "categories": ["vegetarian", "vegan"]
            },
            "vegan": {
                "terms": ["vegan", "vegetarian"],
                "categories": ["vegan", "vegetarian"]
            }
        }
    
    def get_cuisine_terms(self, cuisine: str) -> List[str]:
        """
        Get search terms for a cuisine type.
        
        Args:
            cuisine: Cuisine type (e.g., "pizza", "italian")
            
        Returns:
            List of search terms
        """
        cuisine_lower = cuisine.lower().strip()
        
        if cuisine_lower in self.cuisine_mapping:
            return self.cuisine_mapping[cuisine_lower]["terms"]
        
        # If not found, return the original cuisine as a term
        return [cuisine_lower]
    
    def get_cuisine_categories(self, cuisine: str) -> List[str]:
        """
        Get Yelp categories for a cuisine type.
        
        Args:
            cuisine: Cuisine type
            
        Returns:
            List of Yelp categories
        """
        cuisine_lower = cuisine.lower().strip()
        
        if cuisine_lower in self.cuisine_mapping:
            return self.cuisine_mapping[cuisine_lower]["categories"]
        
        # If not found, return empty list
        return []
    
    def is_cuisine_match(self, place_name: str, place_categories: List[str], cuisine: str) -> bool:
        """
        Check if a place matches the specified cuisine.
        
        Args:
            place_name: Name of the place
            place_categories: Categories of the place
            cuisine: Cuisine to match against
            
        Returns:
            True if place matches cuisine, False otherwise
        """
        cuisine_lower = cuisine.lower().strip()
        place_name_lower = place_name.lower()
        
        # Check if cuisine appears in place name
        if cuisine_lower in place_name_lower:
            return True
        
        # Check if cuisine categories match place categories
        cuisine_categories = self.get_cuisine_categories(cuisine)
        place_categories_lower = [cat.lower() for cat in place_categories]
        
        for cuisine_cat in cuisine_categories:
            if cuisine_cat in place_categories_lower:
                return True
        
        return False
    
    def get_primary_search_term(self, cuisine: str) -> str:
        """
        Get the primary search term for a cuisine.
        
        Args:
            cuisine: Cuisine type
            
        Returns:
            Primary search term
        """
        terms = self.get_cuisine_terms(cuisine)
        return terms[0] if terms else cuisine.lower()

# Global instance
cuisine_mapper = CuisineMapper() 