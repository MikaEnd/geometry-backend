from core.handlers.base_handler import BaseHandler
from core.llm.llm_client import ask_gpt
from core.skills.multi_step_task import MultiStepTaskSkill
from core.router.llm_router import resolve_task

class ManagerHandler(BaseHandler):
    def __init__(self):
        self.pending_tasks = {}

    async def handle(self, user_id: str, message: str) -> str:
        # Ответ на уточнение
        if user_id in self.pending_tasks:
            task = self.pending_tasks.pop(user_id)
            full_message = f"{task['original_task']}. Уточнение: {message}"
            mode, handler = await resolve_task(user_id, full_message)

            if mode == "complex":
                return await MultiStepTaskSkill().execute(user_id, full_message)
            elif mode == "clarify":
                return "🔄 Нужна дополнительная информация. Попробуй сформулировать точнее."
            elif handler:
                return await handler.handle(user_id, full_message)
            return "❌ Не удалось запустить исполнителя после уточнения."

        # Основной вызов — без уточнения
        mode, handler = await resolve_task(user_id, message)

        if mode == "complex":
            return await MultiStepTaskSkill().execute(user_id, message)

        if mode == "clarify":
            clarification = await ask_gpt(
                f"Пользователь задал: '{message}'. Какие 1–2 вопроса нужно уточнить, чтобы выбрать исполнителя?"
            )
            self.pending_tasks[user_id] = {
                "original_task": message,
                "clarification": clarification
            }
            return f"Чтобы понять задачу, уточни, пожалуйста:\n{clarification}"

        if handler:
            return await handler.handle(user_id, message)

        return "⚠️ Не удалось обработать запрос. Возможно, ошибка компетенции."
