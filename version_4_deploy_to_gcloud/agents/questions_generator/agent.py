"""
File: agents/questions_generator/agent.py
Purpose: Defines the Questions Generator Agent that takes a user-provided topic and generates 
         five important questions to help understand that topic. This agent uses Google search 
         to research the topic before generating informed questions.

This is the first agent in the website building pipeline that:
1. Receives a topic from the user
2. Researches the topic using Google search
3. Generates exactly 5 questions that help understand the topic
4. Outputs the questions for the questions_researcher agents to answer
"""

# Import required system modules for path manipulation
import os  # Operating system interface for file paths
import sys  # System-specific parameters and functions

# Import the main LlmAgent class from Google ADK (Agent Development Kit)
from google.adk.agents import LlmAgent  # Core agent class for creating LLM-based agents

# Import Google search tool that allows the agent to perform web searches
from google.adk.tools import google_search  # Pre-built tool for Google search functionality

# Add the project root directory to Python path so we can import utility modules
# This allows importing from the utils directory two levels up from current file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..")))

# Import utility function to load instruction files from text files
from utils.file_loader import load_instructions_file  # Helper to read instruction text files

# Create the Questions Generator Agent instance
questions_generator_agent = LlmAgent(
    # Agent identifier - unique name for this agent in the system
    name = "questions_generator_agent",
    
    # AI model to use - Gemini 2.5 Flash Lite for fast, high-quality responses
    model = "gemini-2.5-flash",
    
    # Load detailed instructions from external text file
    # This keeps the code clean and allows easy modification of agent behavior
    instruction=load_instructions_file("agents/questions_generator/instructions.txt"),
    
    # Load agent description from external text file
    # Provides a brief summary of what this agent does
    description=load_instructions_file("agents/questions_generator/description.txt"),
    
    # Tools available to this agent - Google search for researching topics
    # This allows the agent to gather current information before generating questions
    tools=[google_search],
    
    # Output key - where this agent stores its results in the session state
    # Other agents in the pipeline will reference this key to access the generated questions
    output_key="questions_generator_output"
)