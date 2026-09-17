from pathlib import Path
from time import time
from typing import Generator, Iterable

import yaml
from assistant import Assistant
from config import Config, load_config
from db import get_collection
from pydantic import BaseModel
from store_data_in_chroma import ingest


def generate_chunking_configs(chunk_sizes: Iterable) -> Generator[Config]:
    for chunk_size in chunk_sizes:
        config = load_config()
        config.chunking.chunk_size = chunk_size
        config.chromadb.db_path = f"./data/chroma_{chunk_size}/"
        yield config


def ingest_with_different_chunking():
    for config in generate_chunking_configs([
        100, 200, 500, 1000, 2000, 5000
    ]):
        print("=" * 40)
        print(f"Ingesting with chunk size: {config.chunking.chunk_size}")
        print(f"DB Path: {config.chromadb.db_path}")
        print("=" * 40, end="\n\n")

        collection = get_collection(config)
        ingest(config, collection)


class Question(BaseModel):
    id: str
    group: str
    question: str
    expected_answer: str
    sources: list[str]


def get_test_questions_list() -> list[Question]:
    raw = yaml.safe_load(Path("eval_questions.yaml").read_text(encoding="utf-8"))
    return [Question(**question_raw) for question_raw in raw["questions"]]


def test_different_chunking():
    report = []
    for config in generate_chunking_configs([
        100, 200, 500, 1000, 2000, 5000
    ]):

        print("=" * 40)
        print(f"Testing assistant with chunk size: {config.chunking.chunk_size}")
        print("=" * 40, end="\n\n")

        assistant = Assistant(config)
        question_reports = []
        for question in get_test_questions_list():
            print(f"== Question: {question.question}")
            print(f"== Expected answer:\n{question.expected_answer}")
            t_start = time()
            response = assistant.ask(question.question)
            print(f"== Assistant answer:\n{response.message.content}")
            time_to_response = time() - t_start
            print(f"== Time to response: {time_to_response}")
            question_reports.append({
                "question": question.question,
                "expected_answer": question.expected_answer,
                "assistant_answer": response.message.content,
                "time_to_response": time_to_response,
                "id": question.id,
                "group": question.group,
            })
            print()
        report.append({
            "chunking": config.chunking.chunk_size,
            "questions": question_reports
        })
        with open("test_different_chunking_report.yaml", "w", encoding="utf-8") as fd:
            yaml.safe_dump(report, fd, allow_unicode=True)
            print('==== Report update ====')


if __name__ == "__main__":
    ingest_with_different_chunking()
    test_different_chunking()
