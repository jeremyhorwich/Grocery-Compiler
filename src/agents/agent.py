import os
from dotenv import load_dotenv
from typing import Callable
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

class Agent:
    def __init__(
            self, 
            name: str, 
            tools: list[Callable] | None = None,
            temperature: float = 0.0
    ):
        if tools is None:
            tools = []

        self.llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            temperature=temperature,
            anthropic_api_key=ANTHROPIC_API_KEY
        )

        self.instructions = self.retrieve_instructions(name)
        self.agent = create_agent(
            model=self.llm,
            tools=tools,
            system_prompt=self.instructions
        )

    def retrieve_instructions(self, filename: str) -> str:
        """Read a file."""
        filepath = filename.replace('.', os.sep) + '.txt'
        with open(filepath, "r") as f:
            contents = f.read()
            return contents
        
    def invoke(self, inputs: dict) -> dict:
        """Invoke the agent with inputs."""
        return self.agent.invoke(inputs)