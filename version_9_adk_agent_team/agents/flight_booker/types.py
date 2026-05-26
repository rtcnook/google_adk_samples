# Import BaseModel and Field from Pydantic to create robust, typed data schemas.
from pydantic import BaseModel, Field

class FlightInput(BaseModel):
    """
    Input parameters needed to initiate flight booking.
    
    This schema dictates the required and optional inputs for the flight booker agent.
    When this agent is called, the framework validates that these inputs are present, 
    or directs the agent to gather them.
    """
    # Required parameter: destination city name.
    destination: str = Field(description="Target destination city.")
    
    # Required parameter: departure date formatted as a YYYY-MM-DD string.
    departure_date: str = Field(description="YYYY-MM-DD formatted departure date.")
    
    # Optional parameter: defaults to "window".
    # Providing a 'default' value in Pydantic is very helpful: if the caller (or LLM) 
    # doesn't provide this field, it automatically initializes with the default.
    # This prevents validation errors and guides the agent's interactive questions.
    seat_preference: str = Field(default="window", description="Preferred seat layout: window, aisle, or no preference.")

class FlightOutput(BaseModel):
    """
    Output results of flight booking.
    
    In 'task' mode, the agent is kept active until it can fill all fields in this 
    output schema and return them. This serves as a structural validation boundary 
    confirming that the flight was booked successfully and has an associated code.
    """
    # The unique reservation identifier returned by the flight booking system.
    booking_reference: str = Field(description="The unique airline booking code.")
    
    # The final status of the booking process (e.g., 'confirmed', 'failed').
    status: str = Field(description="Confirmation status of the booking.")
