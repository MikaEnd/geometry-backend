from core.skills.execute_with_llm import ExecuteWithLLMSkill

class DeveloperHandler:
    def __init__(self):
        self.llm_skill = ExecuteWithLLMSkill()

    def can_handle(self, task_description: str) -> bool:
        return self.llm_skill.can_handle(task_description)

    async def handle(self, task_description: str, user_id: str = "anonymous") -> str:
        return await self.llm_skill.execute(user_id, task_description)
