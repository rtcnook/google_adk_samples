"""
Itinerary agent declaration.

Defines the conversational itinerary planner agent using 'chat' mode execution.
"""

# Import pathlib for dynamic file location resolution.
import pathlib

# Import the core Agent class from Google ADK.
from google.adk.agents import Agent

# Import tools available for this agent to execute.
from .tools import search_local_attractions

# --- Dynamic Path Resolution ---
# Resolve the local file folder path dynamically.
current_dir = pathlib.Path(__file__).parent.resolve()
instruction_path = current_dir / "instruction.txt"

# Safely open and read the raw instructions file.
with open(instruction_path, "r", encoding="utf-8") as f:
    instruction_text = f.read()

# --- Agent Declaration ---
root_agent = Agent(
    # Unique name for system orchestration.
    name="itinerary_agent",
    
    # 'chat' mode: This mode allows open-ended, multi-turn, free-form dialogues.
    # Unlike 'single_turn' (which returns immediately) or 'task' (which requires satisfying 
    # a specific output schema), 'chat' mode behaves like a standard chatbot. It allows 
    # conversational brainstorming back-and-forth indefinitely, and relies on user satisfaction 
    # or system prompts to hand control back to the parent coordinator.
    mode="chat",  # default conversational mode
    
    # System instructions.
    instruction=instruction_text,
    
    # Description used by the coordinator for routing decisions.
    description="协作式中文行程规划子 Agent，负责讨论景点、活动和个性化安排。",
    
    # Register search tool.
    tools=[search_local_attractions],
)
