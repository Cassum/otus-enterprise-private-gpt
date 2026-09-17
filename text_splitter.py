from config import Config
from langchain_text_splitters import MarkdownTextSplitter


def get_md_splitter(config: Config) -> MarkdownTextSplitter:
    return MarkdownTextSplitter(
        chunk_size=config.chunking.chunk_size,
        chunk_overlap=config.chunking.chunk_overlap,
    )
