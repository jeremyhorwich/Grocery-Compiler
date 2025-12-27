from agents.ingredients import create_ingredients_agent

def main():
    ingredient = create_ingredients_agent()

    result = ingredient.invoke({
        "messages": [
            {"role": "user", "content": "Cheddar, Milk, Eggs"}
        ]
    })

    print(result["messages"][-1].content)

main()