from abc import ABC, abstractmethod

class BaseHandler(ABC):
    @abstractmethod
    def can_handle(self, message: str) -> bool:
        """Проверяет, может ли обработчик взять задачу."""
        pass

    @abstractmethod
    async def handle(self, message: str, user_id: str) -> str:
        """Обрабатывает входящее сообщение от пользователя."""
        pass
