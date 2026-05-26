"""
File: agents/query_generator/__init__.py
Purpose: Package initialization file for the query_generator agent module.
         This file makes the query_generator directory a Python package and
         imports the main agent module to make it accessible when the package is imported.

This allows other modules to import the query_generator_agent using:
from agents.query_generator import agent
or
from agents.query_generator.agent import query_generator_agent
"""

# Import the agent module from the current package
# This makes the query_generator_agent definition available when the package is imported
from . import agent  # Imports agent.py from the same directory