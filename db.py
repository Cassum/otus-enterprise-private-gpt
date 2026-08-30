import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)
from config import load_config

cfg = load_config()

chroma_client = chromadb.PersistentClient(cfg.chromadb.db_path)
ef = OllamaEmbeddingFunction(model_name=cfg.chromadb.embedding_model, timeout=300)
collection = chroma_client.get_or_create_collection(
    name=cfg.chromadb.collection_name,
    embedding_function=ef,
)
