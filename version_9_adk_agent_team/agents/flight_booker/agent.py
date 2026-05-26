"""
Flight booker agent declaration.

Defines the flight booker agent using interactive 'task' mode execution.
"""

# Import pathlib for clean, cross-platform file system path manipulations.
import pathlib

# Import the core Agent class from Google ADK.
from google.adk.agents import Agent

# Import Pydantic validation types for defining inputs/outputs.
from .types import FlightInput, FlightOutput

# Import registered tools that this agent can execute.
from .tools import book_flight

# --- Dynamic Path Resolution ---
# Retrieve the path to this folder dynamically to ensure portability of file references.
current_dir = pathlib.Path(__file__).parent.resolve()
instruction_path = current_dir / "instruction.txt"

# Safely open and read instructions to serve as system prompt.
with open(instruction_path, "r", encoding="utf-8") as f:
    instruction_text = f.read()

# --- Agent Declaration ---
root_agent = Agent(
    # Unique identification handle for this agent.
    name="flight_booker",
    
    # 'task' mode: This mode tells the ADK framework that this agent's goal is 
    # to complete a specific task. Unlike 'single_turn' mode, which returns immediately, 
    # 'task' mode is interactive. It keeps the agent active in the conversation loop, 
    # allowing it to ask the user clarifying questions back-and-forth until it is 
    # fully satisfied with all parameters needed to produce the final FlightOutput.
    mode="task",
    
    # Schemas used to define incoming data boundaries and expected results.
    input_schema=FlightInput,
    output_schema=FlightOutput,
    
    # Provide system instructions/prompts.
    instruction=instruction_text,
    
    # Agent description used by the coordinator for routing decisions.
    description="交互式航班预订子 Agent，负责确认航班信息并处理预订细节。",
    
    # List of functions available to the agent.
    tools=[book_flight],
)
