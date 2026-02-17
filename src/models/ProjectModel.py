from .BaseDataModel import BaseDataModel
from .dp_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    def __init__(self, dp_client):
        super().__init__(dp_client) 
        self.collection=dp_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
    @classmethod
    async def create_instance(cls, dp_client:object):
        instance = cls(dp_client=dp_client)
        await instance.init_collection()
        return instance
        
    async def init_collection(self):
        all_collections = await self.dp_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:   
            self.collection = await self.dp_client.create_collection(DataBaseEnum.COLLECTION_PROJECT_NAME.value)
            indexes=Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],name=index["name"],unique=index["unique"]
                )

         
      
       
    async def create_project(self, project: Project) :
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        project.id = result.inserted_id
        return project
    
    async def get_project_or_create_one(self, project_id: str):
         record=await self.collection.find_one({"project_id": project_id})
         if record is None:
            project=Project(project_id=project_id)
            project=await self.create_project(project)
            return project
         return Project(**record)
    
    async def get_all_projects(self,page:int=1, page_size:int=10):
        #claclate total documents
        total_documents=await self.collection.count_documents({})    
        #calculate total pages
        total_pages=(total_documents //page_size)
        if total_documents % page_size >0:
            total_pages +=1
        cursor=self.collection.skip((page-1)*page_size).limit(page_size)
        projects=[]
        async for document in cursor:
            projects.append(Project(**document))
        return projects, total_pages