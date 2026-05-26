"""
Multi-agent travel planning team using Google ADK v2.

This is the top-level package initializing our multi-agent directory.
Under Google ADK v2, hierarchical systems are built around a coordinator-worker 
architecture where:
1. A master Coordinator Agent (e.g., travel_planner) acts as the main supervisor.
2. Worker Subagents (e.g., weather_checker, flight_booker, itinerary_agent) are specialized 
   to handle specific tasks using different interaction modes:
   - 'single_turn' for fast background processing.
   - 'task' for interactive, schema-bounded form-filling.
   - 'chat' for open-ended collaborative conversations.
"""
