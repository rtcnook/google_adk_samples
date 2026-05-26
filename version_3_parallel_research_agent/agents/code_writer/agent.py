"""
File: agents/code_writer/agent.py
Purpose: Defines the Code Writer Agent that transforms visual design specifications into
         complete, functional HTML/CSS/JavaScript code. This agent acts as a skilled
         front-end developer, implementing the design system and specifications into
         a single-file webpage that matches the original requirements exactly.

This is the sixth and final agent in the website building pipeline that:
1. Receives detailed design specifications from the designer agent
2. Implements the global design system (colors, typography, spacing) in CSS
3. Converts design specifications into semantic HTML structure
4. Adds interactive functionality with JavaScript where needed
5. Writes the complete webpage to a file using the file_writer_tool
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

# Import the file writing tool that allows the agent to save the generated webpage
from tools.file_writer_tool import write_to_file  # Custom tool for writing HTML files to disk

# Create the Code Writer Agent instance
code_writer_agent = LlmAgent(
    # Agent identifier - unique name for this agent in the system
    name = "code_writer_agent",
    
    # AI model to use - Gemini 2.5 Flash for sophisticated code generation and implementation
    # Uses 2.5 for advanced HTML/CSS/JS generation and design system implementation
    model = "gemini-2.5-flash",
    
    # Load detailed instructions from external text file
    # Instructions contain systematic approach for converting design specs to working code
    # Includes guidelines for semantic HTML, responsive CSS, and interactive JavaScript
    instruction=load_instructions_file("agents/code_writer/instructions.txt"),
    
    # Load agent description from external text file
    # Provides a brief summary of this agent's front-end developer role
    description=load_instructions_file("agents/code_writer/description.txt"),
    
    # Tools available to this agent - file writing capability for saving the generated webpage
    # The write_to_file tool allows the agent to save the complete HTML/CSS/JS to disk
    tools=[write_to_file],
    
    # No output_key needed - this is the final agent that produces the actual webpage file
    # The file_writer_tool handles the final output by writing directly to the filesystem
)