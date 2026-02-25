from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "file_validate_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROCESSING_SUCCESS = "processing_success"
    PROCESSING_FAILED = "processing_failed"
    NO_FILES_ERROR="not_found_files"
    FILE_ID_ERROR="no_file_Found_with_this_id"
    PROJECT_NOT_FOUND="project_not_found"
    INSERT_INTO_VECTORDB_ERROR="failed_to_index_into_vector_db"
    INSERT_INTO_VECTORDB_SUCCESS="successfully_indexed_into_vector_db"
    VERCTORDB_COLLECTION_RETRIEVED="vectordb_collection_retrieved"
    VERCTORDB_COLLECTION_NOT_FOUND="vectordb_collection_not_found"
    VERCTORDB_SEARCH_SUCCESS="vectordb_search_success"
    VERCTORDB_SEARCH_FAILED="vectordb_search_failed"
    RAG_ANSWER_ERROR="rag_answer_generation_error"
    RAG_ANSWER_SUCCESS="rag_answer_generated_successfully"
    

    
