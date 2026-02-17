from .BaseDataModel import BaseDataModel
from .dp_schemes import DataChunk, Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId
class AssetModel(BaseDataModel):
    def __init__(self, dp_client):
        super().__init__(dp_client=dp_client)  
        self.collection=self.dp_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
    
    async def init_collection(self):
        all_collections = await self.dp_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:   
            self.collection = await self.dp_client.create_collection(DataBaseEnum.COLLECTION_ASSET_NAME.value)
            indexes=DataChunk.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],name=index["name"],unique=index["unique"]   )
    @classmethod
    async def create_instance(cls, dp_client:object):
        instance = cls(dp_client=dp_client)
        await instance.init_collection()
        return instance   
    
    async def create_asset(self, asset: Asset) :   
        result = await self.collection.insert_one(asset.dict(by_alias=True, exclude_unset=True))
        asset.id = result.inserted_id
        return asset
    async def get_all_project_assets(self,asset_project_id: str,asset_type:str):
         records=await self.collection.find({"asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,"asset_type":asset_type}
                                           ).to_list(length=None)

       
         return  [  Asset(**record) for record in records ]
    async def get_asset_record(self,asset_project_id: str,asset_name:str):
         record=await self.collection.find_one({"asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
                                                "asset_name":asset_name }
                                           )
         if record :
              return  Asset(**record)  
         return None
         
       
         
    
