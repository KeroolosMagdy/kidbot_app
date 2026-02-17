from .BaseDataModel import BaseDataModel
from .dp_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId
from pymongo import InsertOne

class ChunkModel(BaseDataModel):
    def __init__(self, dp_client):
        super().__init__(dp_client=dp_client)  
        self.collection=self.dp_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
    @classmethod
    async def create_instance(cls, dp_client:object):
        instance = cls(dp_client=dp_client)
        await instance.init_collection()
        return instance   
    async def init_collection(self):
        all_collections = await self.dp_client.list_collection_names()
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:   
            self.collection = await self.dp_client.create_collection(DataBaseEnum.COLLECTION_CHUNK_NAME.value)
            indexes=DataChunk.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],name=index["name"],unique=index["unique"]
                )


    async def create_chunk(self, chunk: DataChunk) :
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        chunk._id = result.inserted_id

        return chunk
    async def get_chunks(self,chunk_id: str):
         result=await self.collection.find_one({"_id": ObjectId(chunk_id)})
         if result is None:
            return None
         return DataChunk(**result)
    
    async def insert_many_chunks(self,chunks: list,batch_size: int=1000): 
        for i in range(0,len(chunks),batch_size):
            batch=chunks[i:i+batch_size]
        
            operations=[InsertOne(chunk.dict(by_alias=True, exclude_unset=True)) for chunk in batch]
            result = await self.collection.bulk_write(operations)
        return len(chunks)
    
    async def delete_chunks_by_project_id(self, project_id:ObjectId):
        project_id = ObjectId(project_id)
        result = await self.collection.delete_many({"chunk_project_id": project_id})
        return result.deleted_count

