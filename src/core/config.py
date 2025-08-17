from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    All LLM-related parameters are now grouped here.
    """
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_provider: str = "ollama"  # The active LLM provider.

    # Group all LLM-specific parameters.
    # The keys match the parameter names expected by the LLM classes.
    ollama_model: str = "codellama"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    
    # You could add parameters for a new provider like this:
    # anthropic_api_key: str | None = None
    # anthropic_model: str = "claude-3-opus-20240229"

settings = Settings()