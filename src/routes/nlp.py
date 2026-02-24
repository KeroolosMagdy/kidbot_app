from fastapi import FastAPI, APIRouter, Depends, UploadFile, status,Request
from fastapi.responses import JSONResponse
import os   
from .schemes import PushRequest,SearchRequest
from models import ProjectModel,ChunkModel,AssetModel,ResponseSignal
from controllers import NLPController

 
import logging

logger = logging.getLogger('uvicorn.error')
nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1", "nlp"],
)
@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request, project_id: str, push_request: PushRequest):
    project_model = await ProjectModel.create_instance(
      dp_client=request.app.dp_client
    )

    chunk_model = await ChunkModel.create_instance(
     dp_client=request.app.dp_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )
    chunkl_model = await ChunkModel.create_instance(
        dp_client=request.app.dp_client
    )

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.PROJECT_NOT_FOUND.value
            }
        )
    nlp_controller = NLPController(
        vectordb_client=request.app.Vector_client,
        generation_client=request.app.Generation_client,
        embedding_client=request.app.Embedding_client,
        template_parser=None
    )
    has_records= True
    page_no=1
    inserted_items_count=0
    idx=0
    while has_records:

        page_chunks = await chunkl_model.get_poject_chunks(
        project_id=project.id,
        page_no=page_no
    )

        if not page_chunks:
         break

        page_no += 1

        chunk_ids = list(range(idx, idx + len(page_chunks)))
 
        is_inserted = nlp_controller.index_into_vector_db(
        project=project,
        chunks=page_chunks,
        do_reset=push_request.do_reset,
        chunks_ids=chunk_ids
    )

        if not is_inserted:
         logger.error(f"Failed to index project: {project.project_id} into vector db")
         return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "signal": ResponseSignal.INSERT_INTO_VECTORDB_ERROR.value
            }
        )

        inserted_items_count += len(page_chunks)
        idx += len(page_chunks)

# 👇 هنا بقى الصح
    return JSONResponse(
      status_code=status.HTTP_200_OK,
      content={
         "signal": ResponseSignal.INSERT_INTO_VECTORDB_SUCCESS.value,
        "inserted_items_count": inserted_items_count
    }
)


@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request: Request,project_id: str):
    project_model = await ProjectModel.create_instance(
      dp_client=request.app.dp_client
    )
    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )
    nlp_controller = NLPController(
        vectordb_client=request.app.Vector_client,
        generation_client=request.app.Generation_client,
        embedding_client=request.app.Embedding_client,
        template_parser=None
    )
    collection_info = nlp_controller.get_vector_db_collection_info(project=project)
    return JSONResponse(
      status_code=status.HTTP_200_OK,
      content={
         "signal": ResponseSignal.VERCTORDB_COLLECTION_RETRIEVED.value,
        "collection_info": collection_info
    }
)
@nlp_router.post("/index/search/{project_id}")
async def search_index(request: Request,project_id: str,search_request:SearchRequest):
    project_model = await ProjectModel.create_instance(
      dp_client=request.app.dp_client
    )
    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )
    nlp_controller = NLPController(
        vectordb_client=request.app.Vector_client,
        generation_client=request.app.Generation_client,
        embedding_client=request.app.Embedding_client,
        template_parser=None
    )
    results = nlp_controller.search_verctor_db_collection(
        project=project,
        text=search_request.text,
        limit=search_request.limit
    )
    if not results:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "signal": ResponseSignal.VERCTORDB_SEARCH_FAILED.value
            }
        )
          
    return JSONResponse(
        content={
            "signal": ResponseSignal.VERCTORDB_SEARCH_SUCCESS.value,
            "results": results
        }
    )
 

  
      

