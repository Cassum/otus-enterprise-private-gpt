from config import load_config
from langchain_text_splitters import MarkdownTextSplitter

cfg = load_config()
splitter = MarkdownTextSplitter(
    chunk_size=cfg.chunking.chunk_size,
    chunk_overlap=cfg.chunking.chunk_overlap,
)
