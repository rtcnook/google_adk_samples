"""
File: agents/query_generator/agent.py
Purpose: Defines the Query Generator Agent that synthesizes and merges research outputs from
         all five question researcher agents into a single, comprehensive query for webpage
         development. This agent acts as a bridge between the research phase and the 
         requirements writing phase of the website building pipeline.

This is the third agent in the website building pipeline that:
1. Receives research outputs from all 5 question researcher agents
2. Analyzes and synthesizes the research findings
3. Transforms research insights into web development context
4. Creates a single comprehensive query for the requirements writer
5. Outputs the merged query for webpage requirement generation
"""

# Import required system modules for path manipulation
import os  # Operating system interface for file paths
import sys  # System-specific parameters and functions

# Import the main LlmAgent class from Google ADK (Agent Development Kit)
from google.adk.agents import LlmAgent  # Core agent class for creating LLM-based agents

# Add the project root directory to Python path so we can import utility modules
# This allows importing from the utils directory two levels up from current file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..")))

# Import utility function to load instruction files from text files
from utils.file_loader import load_instructions_file  # Helper to read instruction text files

# Create the Query Generator Agent instance
query_generator_agent = LlmAgent(
    # Agent identifier - unique name for this agent in the system
    name = "query_generator_agent",
    
    # AI model to use - Gemini 2.5 Flash Lite for fast, high-quality synthesis
    model = "gemini-2.5-flash",
    
    # Load detailed instructions from external text file
    # Instructions contain logic for synthesizing multiple research outputs into one query
    instruction=load_instructions_file("agents/query_generator/instructions.txt"),
    
    # Load agent description from external text file
    # Provides a brief summary of this agent's synthesis and merging role
    description=load_instructions_file("agents/query_generator/description.txt"),
    
    # No tools needed - this agent works purely with text synthesis and analysis
    # It processes the research outputs from previous agents without external API calls
    
    # Output key - where this agent stores the merged query in the session state
    # The requirements_writer agent will reference this key to get the comprehensive query
    output_key="merged_query_output"
)