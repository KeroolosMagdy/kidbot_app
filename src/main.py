from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from stores.llm.LLMProviderFactory import LLMProviderFactory

 
from helpers.config import get_settings, Settings

app = FastAPI()


async def startup_db_client():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.dp_client = app.mongo_conn[settings.MONGODB_DATABASE]
    llm_provider_factory = LLMProviderFactory(settings)

    #gemeration backend
    app.Generation_client = llm_provider_factory.create(settings.GENERATION_BACKEND)
    app.Generation_client.set_generation_model(settings.GENERATION_MODEL_ID)

     #embedding backend
    app.Embedding_client = llm_provider_factory.create(settings.EMBEDDING_BACKEND)
    app.Embedding_client.set_embedding_model(settings.EMBEDDING_MODEL_ID, settings.EMBEDDING_DEFAULT_MAX_TOKENS)

async def shutdown_db_client():
    app.mongo_conn.close()

app.router.lifespan.onstartup.append(startup_db_client)
app.router.lifespan.onshutdown.append(shutdown_db_client)    
app.include_router(base.base_router)
app.include_router(data.data_router)

