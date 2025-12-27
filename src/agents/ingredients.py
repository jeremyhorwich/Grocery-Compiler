from .agent import Agent
from dotenv import load_dotenv
from langchain.tools import tool
from requests import get, exceptions
import os

load_dotenv()

USDA_API_KEY = os.getenv("USDA_API_KEY")

@tool
def search_usda_database(query: str) -> str:
    """Search the USDA FoodData Central database by food and get FDC IDs."""
    RESULTS_TO_BROWSE = 5

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": USDA_API_KEY,
        "query": query,
        "pageSize": 5,
        "dataType": ["Foundation", "SR Legacy"]
    }

    try:
        response = get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        foods = data.get('foods', [])[:RESULTS_TO_BROWSE]
        
        results = []
        for food in foods:
            desc = food.get('description', 'N/A')
            common = food.get('commonNames', '')
            additional = food.get('additionalDescriptions', '')
            
            extra_info = []
            if common:
                extra_info.append(f"Common: {common}")
            if additional:
                extra_info.append(f"Additional: {additional}")
            
            extra = f" ({', '.join(extra_info)})" if extra_info else ""
            
            results.append(
                f"- {desc}{extra}\n"
                f"  FDC ID: {food.get('fdcId', 'N/A')}, "
                f"Type: {food.get('dataType', 'N/A')}, "
                f"Category: {food.get('foodCategory', 'N/A')}"
            )
        
        if not results:
            return f"No results found for '{query}'"
        
        return f"Search results for '{query}':\n\n" + "\n\n".join(results)
        
    except Exception as e:
        return f"Error searching USDA database: {str(e)}"

@tool
def get_food_details(fdc_id: str) -> str:
    """Get detailed information about a single food item by its FDC ID.
    
    Args:
        fdc_id: The FDC ID of the food item
    """
    url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
    params = {"api_key": USDA_API_KEY}
    
    target_nutrients = {
        # Macronutrients
        "Carbohydrate", "Fiber", "Protein", "Fat", 
        "Saturated fatty acids", "Trans fatty acids",
        "α-Linolenic Acid", "Linoleic Acid", "Cholesterol",
        "Water",
        
        # Vitamins
        "Vitamin A", "Vitamin C", "Vitamin D", "Vitamin B6",
        "Vitamin E", "Vitamin K", "Thiamin", "Vitamin B12",
        "Riboflavin", "Folate", "Niacin", "Choline",
        "Pantothenic Acid", "Biotin",
        
        # Minerals
        "Calcium", "Chloride", "Chromium", "Copper", "Fluoride",
        "Iodine", "Iron", "Magnesium", "Manganese", "Molybdenum",
        "Phosphorus", "Potassium", "Selenium", "Sodium", "Zinc"
    }
    
    try:
        response = get(url, params=params, timeout=60)
        
        if response.status_code == 404:
            return f"Food with FDC ID {fdc_id} not found."
        
        response.raise_for_status()
        data = response.json()

        result = f"""Food Details for FDC ID {fdc_id}:
                - Description: {data.get('description', 'N/A')}
                - Data Type: {data.get('dataType', 'N/A')}
                - Food Category: {data.get('foodCategory', {}).get('description', 'N/A') if isinstance(data.get('foodCategory'), dict) else data.get('foodCategory', 'N/A')}

                Nutrients:
                """
        
        food_nutrients = data.get('foodNutrients', [])
        found_nutrients = []
        
        for fn in food_nutrients:
            nutrient = fn.get('nutrient', {})
            nutrient_name = nutrient.get('name', '')
            
            matched = False
            for target in target_nutrients:
                if target.lower() in nutrient_name.lower():
                    matched = True
                    break
            
            if matched:
                amount = fn.get('amount')
                unit = nutrient.get('unitName', '')
                
                if amount is not None:
                    found_nutrients.append(f"  - {nutrient_name}: {amount} {unit}")
        
        if found_nutrients:
            result += "\n".join(found_nutrients)
        else:
            result += "  No matching nutrients found"
        
        return result
        
    except exceptions.Timeout:
        return f"Error: Request timed out for FDC ID {fdc_id}"
    except exceptions.RequestException as e:
        return f"Error: Network error retrieving FDC ID {fdc_id}: {str(e)}"
    except ValueError as e:
        return f"Error: Invalid JSON response for FDC ID {fdc_id}: {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error retrieving FDC ID {fdc_id}: {str(e)}"

def create_ingredients_agent() -> Agent:
    """Create an ingredient agent."""

    INGREDIENT_AGENT_TEMPERATURE = 0.4

    return Agent(
        __name__, 
        tools=[search_usda_database, get_food_details],
        temperature=INGREDIENT_AGENT_TEMPERATURE
    )