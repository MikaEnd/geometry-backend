from core.skills.execute_with_llm import ExecuteWithLLMSkill

class DeveloperHandler:
    def __init__(self):
        self.llm_skill = ExecuteWithLLMSkill()

    async def handle(self, task_description: str, user_id: str = "anonymous") -> str:
        if self.llm_skill.can_handle(task_description):
            return await self.llm_skill.execute(user_id, task_description)
        return "⚠️ Задача не распознана как разработческая."
