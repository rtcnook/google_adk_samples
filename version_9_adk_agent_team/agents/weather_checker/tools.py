"""
Tools for the weather checker subagent.

In the Google ADK v2 framework, any standard Python function can be registered 
as a 'tool' that an LLM-based agent can call. The ADK framework automatically 
parses the function's docstring, parameter types, and return types to generate 
a tool schema (JSON schema) that is shared with the LLM. Therefore, clear and 
accurate docstrings and type hints are vital.
"""

def geocode_address(address: str) -> str:
    """Geocode a physical address or city name into geographic coordinates.
    
    The LLM reads this docstring to understand:
    1. What the tool does (transforms an address/city name to coordinates).
    2. What arguments it requires (`address` as a string).
    3. What it returns (a string containing coordinates).
    
    Args:
        address: The destination city or address (e.g., "Paris").
        
    Returns:
        A string representation of coordinates or a success/failure message.
    """
    # This is a mock geocoding service representing how a real integration
    # (e.g., using Google Maps Geocoding API) would return coordinates.
    return f"Coordinates for '{address}': 48.8566° N, 2.3522° E"


def get_weather(location: str) -> str:
    """Get the current temperature and weather conditions for a location.
    
    The LLM reads this docstring to understand:
    1. When to call this tool (when it needs weather data for coordinates or a location).
    2. What argument to pass (`location` string).
    
    Args:
        location: The coordinates or destination name (e.g., "Paris").
        
    Returns:
        A formatted string describing the weather.
    """
    # This is a mock weather service representing how a real weather API
    # (e.g., OpenWeatherMap or Tomorrow.io) would return conditions.
    return f"Current weather in {location}: Sunny, 21°C (70°F). Light breeze."
