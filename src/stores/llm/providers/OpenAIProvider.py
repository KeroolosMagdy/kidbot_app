from stores import LLMInterface
from openai import OpenAI
from ..LLMEnum import LLMEnum, OpenAIEnums
import logging
class OpenAIProvider(LLMInterface):
    def __init__(self, api_key: str,api_url: str = None,default_input_max_character: int = 1000,default_generation_max_output_token: int = 1000,deafault_generation_temperature: float = 0.1):
                 
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_character = default_input_max_character
        self.default_generation_max_output_token = default_generation_max_output_token
        self.default_generation_temperature = deafault_generation_temperature

        self.generation_model_id =  None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI (api_key=self.api_key,
                              api_url=self.api_url 
                )
        self.logger= logging.getLogger(__name__)
        

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int ):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def generate_text(self, prompt: str, max_output_tokens: int, chat_history: list=[], temperature: float = None):
        if not self.client:

            self.logger.error("OpenAI client is not initialized.")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Generation model ID is not set.")
            return None
        
        max_output_tokens= max_output_tokens if max_output_tokens  else self.default_generation_max_output_token
        temperature=temperature if temperature  else self.default_generation_temperature
        chat_history.append(self.construct_prompt(prompt=prompt, role=OpenAIEnums.USER.value))

        response = self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature
        )
        if not response or not response.choices or not response.choices[0].message or not response.choices[0].message.content or len(response.choices) == 0:
            self.logger.error("No response or choices received from OpenAI API.")
            return None
        
        return response.choices[0].message.content
    
    def embed_text(self, text: str, document_type: str=None):
        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set.")
            return None
        

            

        response = self.client.embeddings.create(
            input=text,
            model=self.embedding_model_id
        )
        return response.data[0].embedding

    def construct_prompt(self, prompt: str, role:str):
        return {"role": role, 
                "content": prompt}