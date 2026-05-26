"""
Weather checker subagent package.

This __init__.py file marks this directory as a Python package, allowing clean relative 
and absolute imports of its components. 

Exposing the `agent` module directly at the package level simplifies imports in 
other parts of the system, such as in the central coordinator `travel_planner/agent.py`.
"""

# Import the agent module to make it accessible directly when importing the package.
from . import agent
