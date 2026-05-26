"""
Weather checker agent declaration.

This module defines and configures the 'weather_checker' Agent instance, which 
acts as an autonomous background subagent within our travel planning application.
"""

# Import pathlib for clean, cross-platform file system path manipulations.
import pathlib

# Import the core Agent class from the Google ADK library.
# Under the hood, this class manages the integration with the Gemini LLM,
# schema validation, system instructions, and tool calling capabilities.
from google.adk.agents import Agent

# Import the structured schemas (input and output) that define the agent's interface.
from .types import WeatherInput, WeatherOutput

# Import the helper functions (tools) that the agent is allowed to invoke.
from .tools import geocode_address, get_weather

# --- Dynamic Path Resolution ---
# We resolve the absolute path of the directory containing this file.
# This technique ensures that if the agent is run from any other directory 
# (e.g., via the `adk run` command-line tool), it can reliably locate its 
# relative configuration and instruction files.
current_dir = pathlib.Path(__file__).parent.resolve()
instruction_path = current_dir / "instruction.txt"

# Safely open and read the instruction file.
with open(instruction_path, "r", encoding="utf-8") as f:
    instruction_text = f.read()

# --- Agent Declaration ---
# Here, we instantiate the Agent class with its corresponding configuration.
root_agent = Agent(
    # The unique identifying name of this agent.
    name="weather_checker",
    
    # 'single_turn' mode: This mode tells the ADK framework that this agent 
    # executes in a single logical turn (non-interactive background execution). 
    # It receives the structured input (WeatherInput), executes tools autonomously 
    # until it is finished, populates the structured output (WeatherOutput), and 
    # returns immediately without prompting the user for conversational input.
    mode="single_turn",
    
    # Provide the input schema model for validating incoming arguments.
    input_schema=WeatherInput,
    
    # Provide the output schema model to enforce the format of the returned results.
    output_schema=WeatherOutput,
    
    # The system instructions/instructions that steer the model's behavior.
    instruction=instruction_text,
    
    # A clear description of the agent. This is used by parent/coordinator agents 
    # to understand what this subagent is capable of and when to delegate to it.
    description="自主天气检查子 Agent，负责查询目的地天气并用中文返回结果。",
    
    # Register the available tools that this agent is authorized to use.
    tools=[geocode_address, get_weather],
)
