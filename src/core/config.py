from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_provider: str = "ollama"  # Default to Ollama
    ollama_model: str = "llama3"
    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-4o-mini"

settings = Settings()