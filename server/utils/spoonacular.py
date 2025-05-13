import os
import requests

SPOONACULAR_BASE_URL = "https://api.spoonacular.com/recipes"

def fetch_recipes_by_ingredients(ingredients):
    """Fetch recipes from Spoonacular based on ingredients."""
    api_key = os.getenv("SPOONACULAR_API_KEY")
    
    if not api_key:
        return {"error": "Missing Spoonacular API key"}, 500

    params = {
        "apiKey": api_key,
        "ingredients": ingredients,
        "number": 10,  # Limit results to 10
        "ranking": 1
    }

    response = requests.get(f"{SPOONACULAR_BASE_URL}/findByIngredients", params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch recipes from Spoonacular"}, response.status_code
