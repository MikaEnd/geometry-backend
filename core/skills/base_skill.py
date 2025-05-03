from abc import ABC, abstractmethod

class BaseSkill(ABC):
    @abstractmethod
    def can_handle(self, message: str) -> bool:
        pass

    @abstractmethod
    async def execute(self, user_id: str, message: str) -> str:
        pass
