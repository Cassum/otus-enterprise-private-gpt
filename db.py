import chromadb
from config import load_config

cfg = load_config()

chroma_client = chromadb.PersistentClient(cfg.chromadb.db_path)
collection = chroma_client.get_or_create_collection(name=cfg.chromadb.collection_name)
