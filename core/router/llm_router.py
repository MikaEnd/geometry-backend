# core/router/llm_router.py

import asyncio

async def resolve_task(user_id: str, message: str):
    print(f"[DEBUG] user_id={user_id}, message={message}")

    # Имитация логики
    if "папка" in message.lower():
        class DummyHandler:
            async def handle(self, user_id, message):
                return f"Создание папки по запросу: {message}"
        return "normal", DummyHandler()

    return "clarify", None
