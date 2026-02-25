from fastapi import FastAPI
from routes import base, data,nlp
from motor.motor_asyncio import AsyncIOMotorClient
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser
 
from helpers.config import get_settings, Settings

app = FastAPI()


async def startup_span():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.dp_client = app.mongo_conn[settings.MONGODB_DATABASE]
    llm_provider_factory = LLMProviderFactory(settings)
    vector_provider_factory = VectorDBProviderFactory(settings)
    #app.GENERATION_DEFAULT_MAX_TOKENS=Settings.GENERATION_DEFAULT_MAX_TOKENS
    

    #generation backend
    app.Generation_client = llm_provider_factory.create(settings.GENERATION_BACKEND)
    app.Generation_client.set_generation_model(settings.GENERATION_MODEL_ID)

     #embedding backend
    app.Embedding_client = llm_provider_factory.create(settings.EMBEDDING_BACKEND)
    app.Embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID, embedding_size=settings.EMPEDDING_MODEL_SIZE)

     #vector backend
    app.Vector_client = vector_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)
    app.Vector_client.connect()
    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG,
    )

async def shutdown_span():
    app.mongo_conn.close()
    app.Vector_client.disconnect()

    

app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)

