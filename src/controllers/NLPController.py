from .BaseController import BaseController
from models.dp_schemes import Project, DataChunk
from typing import List
from stores.llm import DocumentTypeEnum



class NLPController (BaseController):
     def __init__(self, vectordb_client, generation_client, 
                 embedding_client, template_parser):
        super().__init__()  
        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser


     def create_collection_name(self, project_id: str):
         return f"collection_{project_id}".strip()
     async def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return await self.vectordb_client.delete_collection(collection_name=collection_name)
     
     async def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = await self.vectordb_client.get_collection_info(collection_name=collection_name)

        return collection_info
     
     async def index_into_vector_db(self, project: Project, chunks: List[DataChunk],
                                   chunks_ids: List[int], 
                                   do_reset: bool = False):
         # GET COLLECTION NAME
         collection_name = self.create_collection_name(project_id=project.project_id)
         #MANAGE ITEMS
         texts = [chunk.text for chunk in chunks]
         metadata = [chunk.metadata for chunk in chunks]
         vectors = [self.embedding_client.embed_text(text=text,document_type=DocumentTypeEnum.DOCUMENT.value) for text in texts]
        #CREATE COLLECTION IF NOT EXISTED
         _ = await self.vectordb_client.create_collection(collection_name=collection_name, 
                                                            embedding_size=self.embedding_client.embedding_size,
                                                            do_reset=do_reset)
          # step4: insert into vector db
         _ = await self.vectordb_client.insert_many(
             collection_name=collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
            record_ids=chunks_ids,
        )
