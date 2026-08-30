from pathlib import Path

import yaml
from pydantic import BaseModel


class ChunkingConfig(BaseModel):
    chunk_size: int
    chunk_overlap: int


class LLMConfig(BaseModel):
    model: str
    base_url: str
    temperature: float


class ChromaDBConfig(BaseModel):
    db_path: str
    collection_name: str
    embedding_model: str


class IngestConfig(BaseModel):
    data_path: str

class Config(BaseModel):
    chunking: ChunkingConfig
    llm: LLMConfig
    chromadb: ChromaDBConfig
    ingest: IngestConfig


def load_config(path: str = "config.yaml") -> Config:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return Config(**raw)
