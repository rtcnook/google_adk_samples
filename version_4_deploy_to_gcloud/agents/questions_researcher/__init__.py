"""
File: agents/questions_researcher/__init__.py
Purpose: Package initialization file for the questions_researcher agent module.
         This file makes the questions_researcher directory a Python package and
         imports the main agent module to make it accessible when the package is imported.

This allows other modules to import the questions_researcher_agent using:
from agents.questions_researcher import agent
or
from agents.questions_researcher.agent import questions_researcher_agent
"""

# Import the agent module from the current package
# This makes all agent definitions available when the package is imported
from . import agent  # Imports agent.py from the same directory