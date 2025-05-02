from core.handlers.base_handler import BaseHandler
from core.skills.execute_with_llm import ExecuteWithLLMSkill
from core.services.agent_mediator import delegate_to_another_agent

class DeveloperHandler(BaseHandler):
    async def handle(self, user_id: str, message: str) -> str:
        # Пробуем сгенерировать и выполнить bash-команды через ExecuteWithLLMSkill
        skill = ExecuteWithLLMSkill()
        result = await skill.run(user_id, message)

        # Если результат говорит, что задача не разработческая — делегируем через менеджера
        if "команда не найдена" in result.lower() or "не удалось" in result.lower() or "ошибка" in result.lower():
            return await delegate_to_another_agent("Developer", user_id, message)

        return result
