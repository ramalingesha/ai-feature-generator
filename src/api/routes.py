from fastapi import APIRouter, HTTPException, status
from src.api.schemas import FeatureGenerationRequest, FeatureGenerationResponse
from src.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

@router.post(
    "/generate-feature", 
    response_model=FeatureGenerationResponse,
    summary="Generate a .feature file from a user prompt",
    description="Accepts a plain English prompt and returns a well-structured Gherkin .feature file."
)
async def generate_feature_file(request: FeatureGenerationRequest) -> FeatureGenerationResponse:
    """
    This endpoint processes a user's natural language prompt and
    generates a Gherkin-formatted .feature file.
    
    Args:
        request: The FeatureGenerationRequest object containing the user's prompt.

    Returns:
        A FeatureGenerationResponse object with the generated content.
        
    Raises:
        HTTPException: If the LLM service fails to generate a response.
    """
    try:
        generated_text = await llm_service.generate_content(request.user_prompt)
        return FeatureGenerationResponse(generated_content=generated_text)
    except Exception as e:
        # Log the error for debugging purposes (e.g., using a logger)
        print(f"An error occurred during content generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate content. Please try again."
        )