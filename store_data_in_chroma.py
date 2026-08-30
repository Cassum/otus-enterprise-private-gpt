import os
from typing import Iterable

from config import load_config
from db import collection
from text_splitter import splitter


def store():
    ...


def load_document(file_path: str) -> str:
    with open(file_path, encoding='utf-8') as fd:
        data = fd.read()
    return data


def load_documents(path: str) -> Iterable[str]:
    for dirpath, dirnames, filenames in os.walk(path):
        for fname in filenames:
            try:
                fpath = os.path.join(dirpath, fname)
                yield fpath, load_document(fpath)
            except Exception:
                print(f'Failed!\n{dirpath=}\n{fname=}')
                raise


def ingest(path: str, batch_size: int = 100):
    ids = []
    documents = []
    metadatas = []

    for fpath, doc in load_documents(path):
        parts = splitter.split_text(doc)
        for i, part in enumerate(parts, 1):
            ids.append(f"{fpath} - {i}")
            documents.append(part)
            metadatas.append({
                'file': fpath,
                'part_id': i
            })

    for start in range(0, len(ids), batch_size):
        end = start + batch_size
        collection.add(
            ids=ids[start:end],
            documents=documents[start:end],
            metadatas=metadatas[start:end],
        )


if __name__ == "__main__":
    cfg = load_config()
    ingest(cfg.ingest.data_path)
