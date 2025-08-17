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

class FilePathInput(BaseModel):
    """
    Pydantic model for an API request that takes a file path.
    """
    file_path: str = Field(..., description="Relative file path to the feature file.")

class JsonConversionResponse(BaseModel):
    """
    Pydantic model for the JSON conversion API response.
    """
    parsed_json: dict = Field(..., description="The parsed JSON object from the feature file.")