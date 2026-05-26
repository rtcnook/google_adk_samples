"""
Tools for the itinerary agent subagent.

Contains utility functions registered as tools for the itinerary agent.
The agent uses these tools to retrieve localized points of interest.
"""

def search_local_attractions(city: str) -> str:
    """Retrieve top-rated local attractions and points of interest for a city.
    
    The LLM reads this docstring to understand:
    1. When to search for attractions (e.g., when requested by the user or planning a schedule).
    2. What argument is required (`city` string).
    
    Args:
        city: The city name (e.g., "Paris").
        
    Returns:
        A list of top attractions and descriptions.
    """
    # This is a mock directory representing how a real database or search engine
    # (e.g., Google Places API) would return attraction suggestions for a given city.
    return (
        f"Top attractions in {city}: \n"
        "- The Eiffel Tower (Iconic landmark)\n"
        "- The Louvre Museum (World-class art collection)\n"
        "- Seine River Dinner Cruise (Scenic dining)\n"
        "- Notre-Dame Cathedral (Historic Gothic architecture)"
    )
