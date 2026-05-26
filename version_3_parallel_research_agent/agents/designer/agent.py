"""
File: agents/designer/agent.py
Purpose: Defines the Designer Agent that transforms detailed webpage requirements into
         comprehensive visual design specifications. This agent acts as a pragmatic
         UI/UX designer, converting functional requirements into concrete design
         guidelines that developers can implement without ambiguity.

This is the fifth agent in the website building pipeline that:
1. Receives detailed requirements from the requirements_writer agent
2. Establishes a global design system (colors, typography, spacing)
3. Translates requirements into specific visual design specifications
4. Creates section-by-section design details with exact values
5. Outputs structured design specifications for the code_writer agent
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

# Create the Designer Agent instance
designer_agent = LlmAgent(
    # Agent identifier - unique name for this agent in the system
    name = "designer_agent",
    
    # AI model to use - Gemini 2.5 Flash for sophisticated design analysis and specification
    # Uses 2.5 for advanced visual design reasoning and systematic design system creation
    model = "gemini-2.5-flash",
    
    # Load detailed instructions from external text file
    # Instructions contain systematic approach for creating design systems and visual specs
    # Includes step-by-step logic for translating requirements to concrete design values
    instruction=load_instructions_file("agents/designer/instructions.txt"),
    
    # Load agent description from external text file
    # Provides a brief summary of this agent's UI/UX designer role
    description=load_instructions_file("agents/designer/description.txt"),
    
    # No tools needed - this agent works with pure design analysis and specification generation
    # It processes requirements from requirements_writer without external API calls
    
    # Output key - where this agent stores the design specifications in the session state
    # The code_writer agent will reference this key to get the detailed design guidelines
    output_key="designer_output"
)