import json
import os
from pathlib import Path
import tempfile
from fastapi import APIRouter, HTTPException, status
from src.api.schemas import FeatureGenerationRequest, FeatureGenerationResponse, FilePathInput, JsonConversionResponse
from src.services.llm_service import LLMService
from feature_tdd_starter import parse_and_generate

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
    
@router.post(
    "/parse-feature-to-json",
    response_model=JsonConversionResponse,
    summary="Parse a feature file into a JSON object",
    description="Accepts a relative file path to a .feature file and returns its parsed JSON representation.",
)
async def parse_feature_to_json(
    request: FilePathInput,
) -> JsonConversionResponse:
    """
    Endpoint to parse an existing .feature file to JSON.

    Args:
        request: The FilePathInput containing the relative file path.

    Returns:
        A JsonConversionResponse with the parsed JSON.

    Raises:
        HTTPException: If the file is not found or parsing fails.
    """
    # Create an absolute path from the relative input
    project_root = Path(__file__).parent.parent.parent
    absolute_path = (project_root / request.file_path).resolve()

    # Basic security check to prevent directory traversal
    if not absolute_path.is_relative_to(project_root):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File path is outside the project root directory.",
        )
    
    try:
        # 1. The parser returns a JSON string.
        json_string = parse_and_generate(absolute_path)
        
        # 2. Use json.loads() to convert the JSON string to a Python dictionary.
        parsed_data = json.loads(json_string)
        
        # 3. Pass the dictionary to the response model.
        return JsonConversionResponse(parsed_json=parsed_data)
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found at path: {request.file_path}",
        )
    except (ValueError, json.JSONDecodeError) as e:
        # json.JSONDecodeError is the specific error for invalid JSON.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Parsing error: Invalid JSON output from the library. Details: {e}"
        )


@router.post(
    "/generate-and-parse",
    response_model=JsonConversionResponse,
    summary="Generate a feature file and immediately convert it to JSON",
    description="Uses an LLM to create a .feature file from a user prompt, saves it temporarily, and returns the parsed JSON.",
)
async def generate_and_parse(
    request: FeatureGenerationRequest,
) -> JsonConversionResponse:
    """
    Endpoint that combines LLM generation and JSON parsing.

    Args:
        request: The FeatureGenerationRequest containing the user's prompt.

    Returns:
        A JsonConversionResponse with the generated and parsed JSON content.

    Raises:
        HTTPException: If generation or parsing fails.
    """
    # Use a try-finally block to ensure the temporary file is always removed.
    print(request.user_prompt)
    temp_file_path = None
    try:
        # Step 1: Generate .feature content from the LLM
        generated_content = await llm_service.generate_content(request.user_prompt)

        # Step 2: Use a temporary file for the generated content
        with tempfile.NamedTemporaryFile(
            mode="w+", delete=False, suffix=".feature", encoding="utf-8"
        ) as temp_file:
            temp_file.write(generated_content)
            temp_file_path = Path(temp_file.name)
            
            # The flush() call ensures the content is written to disk immediately
            temp_file.flush()
        
        # ... (remaining parsing and response code) ...
        json_string = parse_and_generate(temp_file_path)
        parsed_data = json.loads(json_string)
        return JsonConversionResponse(parsed_json=parsed_data)

    except Exception as e:
        print(f"An error occurred: {e}")
        # Reraise a proper HTTP exception with a general error message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate and parse content. Please check the logs for more details."
        )
    finally:
        # Clean up the temporary file
        if temp_file_path and temp_file_path.exists():
            os.remove(temp_file_path)
            print(f"Temporary file removed: {temp_file_path}")