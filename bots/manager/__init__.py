from core.interfaces import BotHandler
from bots.lawyer import LawyerHandler
from bots.developer import DeveloperHandler
from bots.web_researcher import WebResearcherHandler
from bots.llm_assistant import LLMHandler

class ManagerHandler(BotHandler):
    def __init__(self):
        self.known_handlers = {
            "lawyer": LawyerHandler(),
            "developer": DeveloperHandler(),
            "web_researcher": WebResearcherHandler(),
        }
        self.fallback_handler = LLMHandler()

    def can_handle(self, task_description: str) -> bool:
        return True  # fallback

    def handle(self, task_description: str) -> dict:
        competence = self.guess_competence(task_description)

        if competence in self.known_handlers:
            return {
                "result": f"🧭 Менеджер зафиксировал задачу: {task_description}",
                "next": f"🔎 Возможная компетенция: {competence}. Уточните цель задачи, чтобы делегировать."
            }

        # 1. Компетенция не найдена — инициируем создание нового суб-бота
        spec_prompt = f"""Ты — AI-менеджер проекта. Пользователь поставил задачу: "{task_description}".
Определи, какая компетенция требуется, и опиши, как должен выглядеть минимально полезный суб-бот, чтобы выполнить задачу.
Сформулируй это как техническое задание для фулстек-разработчика.
Ответ напиши строго в одном абзаце без Markdown.
"""

        llm_response = self.fallback_handler.ask_llm(spec_prompt)
        if "error" in llm_response:
            return {"error": llm_response["error"]}

        # 2. Передаём это ТЗ разработчику
        dev = self.known_handlers["developer"]
        return {
            "result": f"🧭 Менеджер не нашёл исполнителя для: {task_description}",
            "next": f"🤖 AI сгенерировал ТЗ для создания нового суб-бота.",
            "tech_task": llm_response["text"],
            "developer_response": dev.handle(llm_response["text"])
        }

    def guess_competence(self, task: str) -> str | None:
        task = task.lower()
        if any(word in task for word in ["договор", "контракт", "закон", "юрист"]):
            return "lawyer"
        if any(word in task for word in ["docker", "установи", "код", "создай", "nginx", "init", "postgre"]):
            return "developer"
        if any(word in task for word in ["найди", "поиск", "где", "веб", "google", "яндекс", "интернет"]):
            return "web_researcher"
        return None
