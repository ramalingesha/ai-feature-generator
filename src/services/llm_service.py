from typing import cast
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from src.core.config import settings
from src.services.prompts import FEATURE_GENERATION_PROMPT

class LLMService:
    """
    A service to handle interactions with different LLM providers using LangChain.
    It encapsulates the logic for selecting and invoking the correct model based on configuration.
    """
    def __init__(self) -> None:
        self.llm: BaseChatModel = self._initialize_llm()
        self.chain: Runnable = self._initialize_chain()

    def _initialize_llm(self) -> BaseChatModel:
        """
        Initializes the correct LangChain LLM instance based on the
        LLM_PROVIDER setting in the environment.
        """
        if settings.llm_provider == "ollama":
            # For Ollama, the server must be running locally.
            return ChatOllama(model=settings.ollama_model)
        elif settings.llm_provider == "openai":
            # For OpenAI, an API key must be provided in the .env file.
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is not set.")
            return ChatOpenAI(
                api_key=settings.openai_api_key,
                model=settings.openai_model
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
            
    def _initialize_chain(self) -> Runnable:
        """
        Creates a LangChain chain by combining the prompt template and the LLM.
        The chain handles the entire process from receiving input to generating output.
        """
        # The chain combines the prompt template with the language model.
        # The .with_type() method is used for strict type hinting of inputs/outputs.
        return (
            cast(ChatPromptTemplate, FEATURE_GENERATION_PROMPT).with_types(
                input_type=dict
            )
            | self.llm
        )

    async def generate_content(self, user_prompt: str) -> str:
        """
        Generates content by invoking the LangChain chain with the user's prompt.
        
        Args:
            user_prompt: The user's input string.

        Returns:
            The generated string from the LLM.
        """
        # Using ainvoke() for asynchronous calls, which is essential for FastAPI.
        response = await self.chain.ainvoke({"user_prompt": user_prompt})
        return response.content