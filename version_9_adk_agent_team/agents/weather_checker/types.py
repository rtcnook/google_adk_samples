# Import BaseModel from Pydantic, which is the base class for creating structured data schemas.
# Import Field from Pydantic, which allows us to add descriptions, default values, and other validation metadata to model fields.
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    """
    Structured input schema for the weather checker agent.
    
    In the Google ADK v2 framework, when an agent has an `input_schema` defined, 
    the framework (and the underlying LLM) uses this Pydantic model to structure 
    and validate the inputs being passed to the agent.
    """
    # The destination parameter is a string. We use Field with a description.
    # The 'description' parameter in Field is critically important: it is passed 
    # directly to the LLM's system instructions as schema metadata, helping the 
    # model understand exactly what value it needs to provide for this field.
    destination: str = Field(description="The target city or destination for the weather check.")

class WeatherOutput(BaseModel):
    """
    Structured output schema for the weather checker agent.
    
    This defines the exact structured JSON format that this agent guarantees to 
    return upon completion of its execution. Defining a structured output schema 
    ensures high reliability when transferring data between different agents.
    """
    # Each field represents a piece of information that the agent is expected to populate.
    # The 'description' guides the LLM on what information should be assigned to each field.
    location: str = Field(description="The city or place name checked.")
    temperature: str = Field(description="Formatted temperature string.")
    conditions: str = Field(description="General weather conditions summary.")
