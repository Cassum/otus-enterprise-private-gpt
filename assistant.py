import ollama

from config import load_config, Config
from db import get_collection

config = load_config()

SYSTEM_PROMPT_TEMPLATE = """
Ты корпоративный ассистент по внутренней базе знаний Ultralitics. Отвечай на вопрос пользователя ТОЛЬКО опираясь на следующий контекст:

{context}

Если ответа в контексте нет, скажи, что не знаешь."""

CONTEXT_ITEM_TEMPLATE = """filename: {filename}
part: {part_id}

{document}"""



class Assistant:

    def __init__(self, config: Config):
        self.model = config.llm.model
        self.collection = get_collection(config)

    def ask(self, question: str, stream=False) -> ollama.ChatResponse:
        context = self.prepare_context(question)
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_TEMPLATE.format(context=context)},
                {"role": "user", "content": question},
            ],
            think=False,
            stream=stream,
        )
        return response

    def prepare_context(self, question: str):
        context_parts = []
        query_result = self.collection.query(query_texts=[question])
        for _id, document, metadata in zip(query_result["ids"][0],
                                           query_result["documents"][0],
                                           query_result["metadatas"][0]):
            context_item = CONTEXT_ITEM_TEMPLATE.format(
                filename=metadata["file"],
                part_id=metadata["part_id"],
                document=document,
            )
            context_parts.append(context_item)
        context_delimiter = "\n\n" + "="*40 + "\n\n"
        return context_delimiter.join(context_parts)


if __name__ == "__main__":
    assistant = Assistant(load_config())
    print(assistant.ask("What improvement options are accessible for workers of the company?"))
