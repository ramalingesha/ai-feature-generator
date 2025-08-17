from typing import Any, Dict, Type
from langchain_core.language_models import BaseChatModel
from src.core.config import settings
from src.services.llm_registry import LLM_PROVIDER_REGISTRY, ProviderConfig

class LLMFactory:
    """
    A factory class for creating the correct LLM adapter instance.
    It is now purely configuration-driven, with no hardcoded logic for providers.
    """
    @staticmethod
    def get_llm() -> BaseChatModel:
        """
        Returns an instance of the chosen LLM based on the application's
        configuration and the provider registry.
        """
        provider_name = settings.llm_provider
        
        provider_config: ProviderConfig | None = LLM_PROVIDER_REGISTRY.get(provider_name)

        if provider_config is None:
            raise ValueError(f"Unsupported LLM provider: '{provider_name}'. Check your registry and .env file.")

        # Extract the class and parameter mapping from the registry.
        provider_class: Type[BaseChatModel] = provider_config["class"]
        param_map: Dict[str, str] = provider_config["params"]
        
        # Build the keyword arguments dictionary dynamically.
        kwargs: Dict[str, Any] = {}
        for constructor_param, settings_attr in param_map.items():
            param_value = getattr(settings, settings_attr, None)
            
            # Raise an error if a required API key is missing.
            if param_value is None and "api_key" in constructor_param:
                raise ValueError(f"API key for '{provider_name}' is not set in the environment.")
            
            kwargs[constructor_param] = param_value

        # Instantiate the LLM class with the dynamically created keyword arguments.
        return provider_class(**kwargs)