from core.interfaces import BotHandler
from bots.lawyer import LawyerHandler
from bots.developer import DeveloperHandler
from bots.web_researcher import WebResearcherHandler
from bots.llm_assistant import LLMHandler
from core.skills.execute_with_llm import ExecuteWithLLMSkill
from core.services.ai_trace_logger import log_trace

class ManagerHandler(BotHandler):
    def __init__(self):
        self.known_handlers = {
            "lawyer": LawyerHandler(),
            "developer": DeveloperHandler(),
            "web_researcher": WebResearcherHandler(),
        }
        self.fallback_handler = LLMHandler()
        self.skill = ExecuteWithLLMSkill()

    def can_handle(self, task_description: str) -> bool:
        return True  # fallback

    async def handle(self, task_description: str, user_id: str) -> str:
        competence = self.guess_competence(task_description)
        handler = self.known_handlers.get(competence)

        log_trace(
            user_id=user_id,
            message=task_description,
            mode="delegate",
            competence=competence,
            handler=handler.__class__.__name__ if handler else None
        )

        if handler:
            return await handler.handle(task_description, user_id)

        # Компетенция не определена — генерируем ТЗ
        prompt = f"""Ты — AI-менеджер проекта. Пользователь поставил задачу: "{task_description}". 
Определи, какая компетенция требуется, и опиши, как должен выглядеть минимально полезный суб-бот, чтобы выполнить задачу.
Сформулируй это как техническое задание для фулстек-разработчика. Один абзац, без Markdown."""
        llm_response = self.fallback_handler.ask_llm(prompt)
        if "error" in llm_response:
            return f"⚠️ Ошибка от LLM: {llm_response['error']}"

        dev_handler = self.known_handlers["developer"]
        dev_response = await dev_handler.handle(llm_response["text"], user_id)

        return f"""🧭 Компетенция не распознана. Менеджер сгенерировал ТЗ и делегировал разработчику.
📄 Техническое задание: {llm_response["text"]}
🛠 Ответ от DeveloperHandler: {dev_response}"""

    def guess_competence(self, task: str) -> str | None:
        task = task.lower()
        if any(word in task for word in ["договор", "контракт", "закон", "юрист"]):
            return "lawyer"
        if any(word in task for word in ["docker", "установи", "код", "создай", "nginx", "init", "postgre"]):
            return "developer"
        if any(word in task for word in ["найди", "поиск", "где", "веб", "google", "яндекс", "интернет"]):
            return "web_researcher"
        return None
