from agents.ingredients import create_ingredients_agent
from agents.plan import create_meal_plan_agent
from agents.recipes import create_recipes_agent
from emails import send_email

def main():
    print("Invoking ingredients agent...")

    ingredients_agent = create_ingredients_agent()
    ingredients_result = ingredients_agent.invoke({
        "messages": [
            {"role": "user", "content": "Construct the list, please."}
        ]
    })

    print("Ingredients agent finished...")

    ingredients_result_content = ingredients_result["messages"][-1].content

    print("Invoking meal plan agent...")

    meal_plan_agent = create_meal_plan_agent()
    meal_plan_result = meal_plan_agent.invoke({
        "messages": [
            {"role": "user", "content": ingredients_result_content}
        ]
    })

    print("Meal plan agent finished...")

    meal_plan_content = meal_plan_result["messages"][-1].content
   
    meal_plan_text_split = meal_plan_content.split("++++++", 1)
    if len(meal_plan_text_split) != 2:
        print("Error: Unexpected recipes agent output format.")
        print(meal_plan_content)
        return
    send_email(meal_plan_text_split[0])

    print("Invoking recipes agent...")

    recipes_agent = create_recipes_agent()
    recipes_result = recipes_agent.invoke({
        "messages": [
            {"role": "user", "content": meal_plan_text_split[1]}
        ]
    })

    print("Recipes agent finished...")
    
    print(recipes_result["messages"][-1].content)

main()