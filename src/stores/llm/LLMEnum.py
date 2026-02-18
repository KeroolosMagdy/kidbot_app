from enum import Enum       
class LLMEnum(Enum):
    """
    Enum for LLM types.
    """
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"

class OpenAIEnums(Enum):
    SYSTEM= "system"
    USER= "user"    
    ASSISTANT= "assistant"
 