from .agent import Agent

def create_recipes_agent() -> Agent:
    """Create an ingredient agent."""

    RECIPES_AGENT_TEMPERATURE = 0.6

    return Agent(
        __name__, 
        temperature=RECIPES_AGENT_TEMPERATURE
    )