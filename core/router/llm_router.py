from core.llm.llm_client import ask_gpt
from core.handlers.routing import get_handler_by_competence
from core.services.auto_handler_generator import create_new_handler
from core.services.ai_trace_logger import log_trace

async def resolve_task(user_id: str, message: str):
    # Определяем, сложная ли задача
    complexity_prompt = (
        f"Требует ли задача многошагового выполнения или декомпозиции?\n"
        f"Задача: {message}\n"
        f"Ответь только: да или нет."
    )
    is_complex = await ask_gpt(complexity_prompt)
    if "да" in is_complex.lower():
        log_trace(user_id, message, "complex", None, None)
        return "complex", None

    # Определяем компетенцию
    competence_prompt = (
        f"На основе запроса определи компетенцию: {message}\n"
        f"Ответь одним словом: разработчик, исследователь, менеджер, документ или неизвестно."
    )
    competence = await ask_gpt(competence_prompt)

    if "неизвестно" in competence.lower():
        log_trace(user_id, message, "clarify", "неизвестно", None)
        return "clarify", None

    handler = get_handler_by_competence(competence)
    if not handler:
        create_new_handler(competence)
        handler = get_handler_by_competence(competence)

    handler_name = handler.__class__.__name__ if handler else "None"
    log_trace(user_id, message, "normal", competence, handler_name)
    return "normal", handler
