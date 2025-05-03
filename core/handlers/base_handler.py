from abc import ABC, abstractmethod
from core.skills.base_skill import BaseSkill

class BaseHandler(ABC):
    def __init__(self):
        self.skills: list[BaseSkill] = []

    async def handle(self, user_id: str, message: str) -> str:
        for skill in self.skills:
            if skill.can_handle(message):
                return await skill.execute(user_id, message)
        return "⚠️ Я не знаю, как выполнить эту задачу."
