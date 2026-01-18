from agents.ingredients import create_ingredients_agent
from agents.plan import create_meal_plan_agent
from agents.recipes import create_recipes_agent
from emails import send_email
import argparse
import os

def main():
    args = parse_args()

    ingredients = ""

    if args.use_cache:
        print("Retrieving ingredients from cache...")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, '..', 'ingredientsCache.txt')
        with open(filepath, "r") as f:
            ingredients = f.read()
    else:
        ingredients = compose_ingredients()

    meal_plan_overview, recipes_prompt = compose_meal_plan(ingredients)
   
    send_email(meal_plan_overview)

    recipes = compose_recipes(recipes_prompt)
    
    print(recipes)

    return


def parse_args():
    parser = argparse.ArgumentParser(description="Grocery Compiler")
    parser.add_argument(
        "--use-cache",
        action="store_true",
        help="Run in test mode"
    )
    return parser.parse_args()


def compose_ingredients():
    print("Invoking ingredients agent...")

    ingredients_agent = create_ingredients_agent()
    ingredients_result = ingredients_agent.invoke({
        "messages": [
            {"role": "user", "content": "Construct the list, please."}
        ]
    })

    print("Ingredients agent finished...")

    return ingredients_result["messages"][-1].content


def compose_meal_plan(ingredients: str = None):
    print("Invoking meal plan agent...")

    meal_plan_agent = create_meal_plan_agent()
    meal_plan_result = meal_plan_agent.invoke({
        "messages": [
            {"role": "user", "content": ingredients}
        ]
    })

    print("Meal plan agent finished...")

    meal_plan_content = meal_plan_result["messages"][-1].content

    meal_plan_text_split = meal_plan_content.split("++++++", 1)
    if len(meal_plan_text_split) != 2:
        print("Error: Unexpected recipes agent output format.")
        print(meal_plan_content)
        return None

    return meal_plan_text_split[0], meal_plan_text_split[1]


def compose_recipes(recipes_prompt: str = None):
    print("Invoking recipes agent...")

    recipes_agent = create_recipes_agent()
    recipes_result = recipes_agent.invoke({
        "messages": [
            {"role": "user", "content": recipes_prompt}
        ]
    })

    print("Recipes agent finished...")

    return recipes_result["messages"][-1].content


if __name__ == "__main__":
    main()