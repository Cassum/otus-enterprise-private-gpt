from pathlib import Path

import yaml
from pydantic import BaseModel, FilePath


class ChunkingConfig(BaseModel):
    chunk_size: int
    chunk_overlap: int


class LLMConfig(BaseModel):
    model: str
    base_url: str
    temperature: float


class ChromaDBConfig(BaseModel):
    db_path: FilePath
    collection_name: str


class Config(BaseModel):
    chunking: ChunkingConfig
    llm: LLMConfig
    chromadb: ChromaDBConfig


def load_config(path: str = "config.yaml") -> Config:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return Config(**raw)