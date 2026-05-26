"""
File: agents/requirements_writer/agent.py
Purpose: Defines the Requirements Writer Agent that transforms a comprehensive, research-based
         query into detailed webpage requirements. This agent acts as an expert technical 
         business analyst, converting high-level concepts into specific, actionable 
         requirements that developers and designers can use to build webpages.

This is the fourth agent in the website building pipeline that:
1. Receives a comprehensive, research-backed query from the query_generator
2. Analyzes the query to identify webpage type and core purpose
3. Breaks down requirements into logical webpage components (Header, Hero, Content, Footer)
4. Defines global requirements (responsiveness, accessibility, SEO)
5. Outputs structured Markdown requirements for the designer agent
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

# Create the Requirements Writer Agent instance
requirements_writer_agent = LlmAgent(
    # Agent identifier - unique name for this agent in the system
    name = "requirements_writer_agent",
    
    # AI model to use - Gemini 2.5 Flash for detailed requirement analysis and generation
    # Note: This uses 2.5 instead of 2.0 for more sophisticated requirement writing
    model = "gemini-2.5-flash",
    
    # Load detailed instructions from external text file
    # Instructions contain systematic approach for converting queries to webpage requirements
    # Includes step-by-step logic for analyzing queries and structuring requirements
    instruction=load_instructions_file("agents/requirements_writer/instructions.txt"),
    
    # Load agent description from external text file
    # Provides a brief summary of this agent's technical business analyst role
    description=load_instructions_file("agents/requirements_writer/description.txt"),
    
    # No tools needed - this agent works with pure text analysis and requirement generation
    # It processes the merged query from query_generator without external API calls
    
    # Output key - where this agent stores the detailed requirements in the session state
    # The designer agent will reference this key to get the structured requirements document
    output_key="requirements_writer_output"
)