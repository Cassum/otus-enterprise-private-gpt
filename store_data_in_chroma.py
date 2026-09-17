import os
from typing import Iterable

import chromadb
from config import Config, load_config
from db import get_collection
from text_splitter import get_md_splitter
from tqdm import tqdm


def load_document(file_path: str) -> str:
    with open(file_path, encoding='utf-8') as fd:
        data = fd.read()
    return data


def load_documents(path: str) -> Iterable[str]:
    for dirpath, _dirnames, filenames in os.walk(path):
        for fname in filenames:
            try:
                fpath = os.path.join(dirpath, fname)
                yield fpath, load_document(fpath)
            except Exception:
                print(f'Failed!\n{dirpath=}\n{fname=}')
                raise


def ingest(config: Config, collection: chromadb.Collection):
    ids = []
    documents = []
    metadatas = []

    print("Splitting documents...")
    for fpath, doc in tqdm(load_documents(config.ingest.data_path)):
        parts = get_md_splitter(config).split_text(doc)
        for i, part in enumerate(parts, 1):
            ids.append(f"{fpath} - {i}")
            documents.append(part)
            metadatas.append({
                'file': fpath,
                'part_id': i
            })

    print("Ingesting...")
    for start in tqdm(range(0, len(ids), config.ingest.batch_size)):
        end = start + config.ingest.batch_size
        collection.add(
            ids=ids[start:end],
            documents=documents[start:end],
            metadatas=metadatas[start:end],
        )
    print("Done\n")


if __name__ == "__main__":
    config = load_config()
    collection = get_collection(config)
    ingest(config, collection)
