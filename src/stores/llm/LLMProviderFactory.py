from . import LLMInterface
from .providers import OpenAIProvider, CohereProvider
from .LLMEnum import LLMEnum
class LLMProviderFactory:

    def __init__(self,config: dict):
        self.config = config


    def create(self,provider_name: str):
        provider_name = provider_name.lower()
        if provider_name == LLMEnum.OPENAI.value:
            api_key = self.config.OPENAI_API_KEY
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_input_max_character=self.config.INPUT_DEFAUKT_MAC_CHARCTERS,
                default_generation_max_output_token=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                deafault_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE

                
                
                )
        elif provider_name == LLMEnum.COHERE.value:

            return CohereProvider(api_key=self.config.COHERE_API_KEY,
                default_input_max_character=self.config.INPUT_DEFAUKT_MAC_CHARCTERS,
                default_generation_max_output_token=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                deafault_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
                                  
                                  
                                  
                                  )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_name}")