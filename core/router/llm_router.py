# core/router/llm_router.py

from core.services.llm import ask_llm
from core.handlers.routing import get_handler_by_competence
from core.services.auto_handler_generator import create_new_handler
from core.services.ai_trace_logger import log_trace

async def resolve_task(user_id: str, message: str):
    # 1. Определяем: нужна ли декомпозиция
    system_prompt = "Ты помощник, который анализирует задачи."
    user_prompt = f"Требует ли задача многошагового выполнения или декомпозиции?\nЗадача: {message}\nОтветь только: да или нет."

    result = ask_llm(system_prompt, user_prompt)
    if result.get("error"):
        return "clarify", None

    answer = result["text"].lower()
    if "да" in answer:
        log_trace(user_id, message, "complex", None, None)
        return "complex", None

    # 2. Определяем компетенцию
    user_prompt = f"На основе запроса определи, кто лучше справится с задачей: разработчик, исследователь, менеджер, документ или неизвестно.\nЗадача: {message}\nОтветь одним словом."
    result = ask_llm(system_prompt, user_prompt)
    if result.get("error"):
        return "clarify", None

    competence = result["text"].lower().strip()

    if "неизвестно" in competence:
        log_trace(user_id, message, "clarify", "неизвестно", None)
        return "clarify", None

    handler = get_handler_by_competence(competence)
    if not handler:
        create_new_handler(competence)
        handler = get_handler_by_competence(competence)

    handler_name = handler.__class__.__name__ if handler else "None"
    log_trace(user_id, message, "normal", competence, handler_name)
    return "normal", handler
