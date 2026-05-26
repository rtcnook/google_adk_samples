"""
Flight booker subagent package.

This file marks the flight_booker directory as a Python package, allowing 
other parts of the program (like the central travel planner coordinator) 
to cleanly import this agent as a modular subcomponent.
"""

# Export the agent module to make it available when importing this package namespace.
from . import agent
