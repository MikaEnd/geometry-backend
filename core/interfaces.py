from abc import ABC, abstractmethod

class Skill(ABC):
    @abstractmethod
    def can_handle(self, message: str) -> bool:
        """Определяет, может ли навык обработать сообщение"""
        pass

    @abstractmethod
    async def execute(self, user_id: str, message: str) -> str:
        """Асинхронно выполняет задачу и возвращает результат"""
        pass
