from core.interfaces import BotHandler
from core.skills.generate_code import GenerateCodeSkill
from core.skills.write_file import WriteFileSkill

class DeveloperHandler(BotHandler):
    def __init__(self):
        self.skills = [
            GenerateCodeSkill(),
            WriteFileSkill(),
        ]

    def can_handle(self, task_description: str) -> bool:
        return any(skill.can_handle(task_description) for skill in self.skills)

    async def handle(self, task_description: str, user_id: str = "anonymous") -> str:
        for skill in self.skills:
            if skill.can_handle(task_description):
                return await skill.execute(user_id, task_description)
        return "🤖 DeveloperHandler не смог обработать запрос."
