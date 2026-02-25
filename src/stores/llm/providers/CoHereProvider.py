from ..import LLMInterface
from ..LLMEnum import  CohereEnums, DocumentTypeEnum
import cohere
import logging
class CohereProvider(LLMInterface): 
     def __init__(self, api_key: str ,
                  default_input_max_character: int = 1000,
                  default_generation_max_output_token: int = 1000,
                  deafault_generation_temperature: float = 0.1):
                 
        self.api_key = api_key
        

        self.default_input_max_character = default_input_max_character
        self.default_generation_max_output_token = default_generation_max_output_token
        self.default_generation_temperature = deafault_generation_temperature

        self.generation_model_id =  None
        self.embedding_model_id = None
        self.embedding_size = None
        self.client = cohere.ClientV2(self.api_key)
        self.logger= logging.getLogger(__name__)
        self.enums=CohereEnums

     def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

     def set_embedding_model(self, model_id: str, embedding_size: int ):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size 

     def process_text(self, text: str):
        return text[:self.default_input_max_character].strip()
    
     def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):

        if not self.client:
            self.logger.error("CoHere client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for CoHere was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_token
        temperature = temperature if temperature else self.default_generation_temperature

        response = self.client.chat(
            model = self.generation_model_id,
            chat_history = chat_history,
            message = self.process_text(prompt),
            temperature = temperature,
            max_tokens = max_output_tokens
        )

        if not response or not response.text:
            self.logger.error("Error while generating text with CoHere")
            return None
        
        return response.text
    
     def construct_prompt(self, prompt: str, role:str):
        return {"role": role, 
                "content":self.process_text( prompt)}
     def embed_text(self, text: str, document_type: str=None):
        if not self.client:
            self.logger.error("Cohere client is not initialized.")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set.")
            return None

        input_type= CohereEnums.DOCUMENT.value if document_type == DocumentTypeEnum.DOCUMENT.value else CohereEnums.QUERY.value
        response = self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_text(text)],
            input_type=input_type,
            embedding_types=["float"]
        )
        if not response or not response.embeddings or not response.embeddings.float_:
            self.logger.error("No embeddings received from Cohere API.")
            return None
        return response.embeddings.float_[0]



        
    