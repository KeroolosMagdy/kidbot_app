from enum import Enum       
class LLMEnum(Enum):
    """
    Enum for LLM types.
    """
    OPENAI = "openai"
    COHERE = "cohere"

class OpenAIEnums(Enum):
    SYSTEM= "system"
    USER= "user"    
    ASSISTANT= "assistant"
 
class CohereEnums(Enum):
    SYSTEM= "SYSTEM"
    USER= "USER"    
    ASSISTANT= "CHATBOT"

    DOCUMENT= "search_document"
    QUERY= "search_query"
class DocumentTypeEnum(Enum):
    """
    Enum for document types.
    """
    DOCUMENT= "document"
    QUERY= "query"