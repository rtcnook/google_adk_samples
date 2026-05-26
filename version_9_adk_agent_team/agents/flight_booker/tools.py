"""
Tools for the flight booker subagent.

Contains standard Python functions registered as tools for the flight booker agent.
The LLM leverages these functions to interact with external mock services or APIs.
"""

def book_flight(destination: str, departure_date: str, seat_preference: str) -> str:
    """Submit a flight booking request with destination, departure date, and seat preference.
    
    The LLM reads this function signature, docstring, and parameter types 
    to know how to call the function when it has accumulated the required arguments.
    
    Args:
        destination: The target destination city.
        departure_date: Date of departure in YYYY-MM-DD format.
        seat_preference: The user's preferred seat (window, aisle, etc.).
        
    Returns:
        A formatted string confirming booking details and reference code.
    """
    # This is a mock representation of an airline's reservation registration backend.
    # It constructs and returns a descriptive string containing booking details 
    # and a simulated reservation code (PAR-9481).
    return (
        f"Flight to {destination} on {departure_date} booked successfully. "
        f"Seat selected: {seat_preference}. Reference Code: PAR-9481"
    )
