"""
File: agents/designer/__init__.py
Purpose: Package initialization file for the designer agent module.
         This file makes the designer directory a Python package and
         imports the main agent module to make it accessible when the package is imported.

This allows other modules to import the designer_agent using:
from agents.designer import agent
or
from agents.designer.agent import designer_agent
"""

# Import the agent module from the current package
# This makes the designer_agent definition available when the package is imported
from . import agent  # Imports agent.py from the same directory