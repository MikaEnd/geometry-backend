from abc import ABC, abstractmethod

class BaseHandler(ABC):
    @abstractmethod
    async def handle(self, message: str, user_id: str) -> str:
        """Обрабатывает входящее сообщение от пользователя."""
        pass
