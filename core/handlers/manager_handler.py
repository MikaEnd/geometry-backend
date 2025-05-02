from core.handlers.base_handler import BaseHandler
from core.llm.llm_client import ask_gpt
from core.skills.execute_with_llm import ExecuteWithLLMSkill
from core.handlers.routing import get_handler_by_competence


class ManagerHandler(BaseHandler):
    def __init__(self):
        self.pending_tasks = {}

    async def handle(self, user_id: str, message: str) -> str:
        if user_id in self.pending_tasks:
            task = self.pending_tasks.pop(user_id)
            full_prompt = f"Изначальная задача: {task['original_task']}\nОтвет на уточнение: {message}\nНа основе этого выбери подходящего исполнителя."
            competence = await ask_gpt(full_prompt + "\nКакая компетенция требуется? (одно слово, например: разработчик, исследователь, менеджер)")
            handler = get_handler_by_competence(competence)
            if handler:
                return await handler.handle(user_id, f"{task['original_task']}. Уточнение: {message}")
            else:
                return f"Задача понята, но подходящей компетенции пока нет: {competence}"
        
        competence = await ask_gpt(f"На основе запроса определи компетенцию: {message}\nОтветь одним словом: разработчик, исследователь, менеджер или неизвестно.")
        
        if "неизвестно" in competence.lower():
            clarification = await ask_gpt(f"Пользователь задал: '{message}'. Какие 1–2 вопроса нужно уточнить, чтобы выбрать исполнителя?")
            self.pending_tasks[user_id] = {
                "original_task": message,
                "clarification": clarification
            }
            return f"Чтобы понять задачу, уточни, пожалуйста:\n{clarification}"
        
        handler = get_handler_by_competence(competence)
        if handler:
            return await handler.handle(user_id, message)
        else:
            return f"Компетенция определена: {competence}, но подходящий исполнитель пока не реализован."
