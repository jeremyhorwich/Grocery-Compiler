from .agent import Agent

def create_meal_plan_agent() -> Agent:
    """Create a meal plan agent."""

    RECIPES_AGENT_TEMPERATURE = 0.6

    return Agent(
        __name__, 
        temperature=RECIPES_AGENT_TEMPERATURE
    )