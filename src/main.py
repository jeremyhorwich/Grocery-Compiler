from agents.ingredients import create_ingredients_agent
from agents.recipes import create_recipes_agent

def main():
    ingredients_agent = create_ingredients_agent()

    ingredients_result = ingredients_agent.invoke({
        "messages": [
            {"role": "user", "content": "Construct the list, please."}
        ]
    })

    ingredients_result_content = ingredients_result["messages"][-1].content

    recipes_agent = create_recipes_agent()

    recipes_result = recipes_agent.invoke({
        "messages": [
            {"role": "user", "content": ingredients_result_content}
        ]
    })

    print(recipes_result["messages"][-1].content)

main()