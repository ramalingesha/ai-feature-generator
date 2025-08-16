from langchain_core.prompts import ChatPromptTemplate

# The system prompt that gives the LLM its role and instructions.
SYSTEM_PROMPT = """
You are an expert software test automation engineer. Your task is to convert simple English use cases into a valid Gherkin syntax and output it as a .feature file. You must always use the keywords Feature, Scenario, Given, When, and Then.
Do not include any extra text, explanations, or code comments. Just provide the Gherkin content.
"""

# Define the overall prompt template using a system message and a placeholder for the user's input.
# This ensures that our system prompt is always correctly formatted and respected by the LLM.
FEATURE_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{user_prompt}"),
    ]
)