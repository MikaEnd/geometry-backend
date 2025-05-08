from bots.lawyer import LawyerHandler
from bots.developer import DeveloperHandler
from bots.web_researcher import WebResearcherHandler
from bots.document import DocumentHandler

from core.skills.execute_with_llm import ExecuteWithLLMSkill
from core.services.llm import ask_llm

class RoutingResult:
    def __init__(self, competence, handler_name, handler):
        self.competence = competence
        self.handler_name = handler_name
        self.handler = handler

def route_task(message: str) -> RoutingResult:
    competence_map = {
        "lawyer": (LawyerHandler, "LawyerHandler"),
        "developer": (DeveloperHandler, "DeveloperHandler"),
        "web_researcher": (WebResearcherHandler, "WebResearcherHandler"),
        "document": (DocumentHandler, "DocumentHandler"),
    }

    prompt = f"""Ты — AI, определяющий, кто должен выполнить задачу.
Вот задание: "{message}"

Выбери одно из направлений:
- developer (код, shell, DevOps, Python)
- lawyer (юридические проверки)
- document (редактирование и генерация docx)
- web_researcher (поиск информации в интернете)

Ответь одним словом — только название компетенции."""

    llm_response = ask_llm(system_prompt=prompt, user_message=message)
    competence = llm_response.get("text", "").strip().lower()

    if competence in competence_map:
        handler_class, name = competence_map[competence]
        return RoutingResult(competence, name, handler_class())

    return RoutingResult(None, None, None)

def get_handler_by_competence(competence: str):
    handlers = {
        "developer": DeveloperHandler,
        "lawyer": LawyerHandler,
        "document": DocumentHandler,
        "web_researcher": WebResearcherHandler,
    }

    handler_class = handlers.get(competence.lower())
    if handler_class:
        return handler_class()
    return None
