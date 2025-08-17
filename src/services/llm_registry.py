from typing import Dict, Type, Any
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

# A type alias for the configuration dictionary.
# It now maps constructor param names (str) to settings attribute names (str).
ProviderConfig = Dict[str, Any]

# Our registry now stores the LLM class and a dictionary of its required parameters,
# where the keys are the constructor's parameter names.
LLM_PROVIDER_REGISTRY: Dict[str, ProviderConfig] = {
    "ollama": {
        "class": ChatOllama,
        "params": {
            "model": "ollama_model"  # Maps constructor param "model" to settings attr "ollama_model"
        }
    },
    "openai": {
        "class": ChatOpenAI,
        "params": {
            "model": "openai_model",
            "api_key": "openai_api_key"
        }
    },
    # To add a new provider, you would simply define its class and parameter mapping here.
    # "anthropic": {
    #     "class": ChatAnthropic,
    #     "params": {
    #         "model": "anthropic_model",
    #         "api_key": "anthropic_api_key"
    #     }
    # },
}