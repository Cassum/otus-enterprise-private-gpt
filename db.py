import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)
from config import Config


def get_collection(config: Config) -> chromadb.Collection:
    chroma_client = chromadb.PersistentClient(config.chromadb.db_path)
    ef = OllamaEmbeddingFunction(model_name=config.chromadb.embedding_model, timeout=300)
    collection = chroma_client.get_or_create_collection(
        name=config.chromadb.collection_name,
        embedding_function=ef,
    )

    return collection
