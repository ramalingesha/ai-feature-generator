from pydantic import BaseModel, Field

class FeatureGenerationRequest(BaseModel):
    """
    Pydantic model for the incoming API request.
    Validates that 'user_prompt' is a non-empty string.
    """
    user_prompt: str = Field(
        ..., 
        min_length=1, 
        description="The user's plain English use case for the .feature file."
    )

class FeatureGenerationResponse(BaseModel):
    """
    Pydantic model for the outgoing API response.
    """
    generated_content: str = Field(
        ..., 
        description="The generated Gherkin content for the .feature file."
    )