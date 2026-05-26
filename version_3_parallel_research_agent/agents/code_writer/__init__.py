"""
File: agents/code_writer/__init__.py
Purpose: Package initialization file for the code_writer agent module.
         This file makes the code_writer directory a Python package and
         imports the main agent module to make it accessible when the package is imported.

This allows other modules to import the code_writer_agent using:
from agents.code_writer import agent
or
from agents.code_writer.agent import code_writer_agent
"""

# Import the agent module from the current package
# This makes the code_writer_agent definition available when the package is imported
from . import agent  # Imports agent.py from the same directory