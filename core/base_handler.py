from abc import ABC, abstractmethod

class BaseHandler(ABC):
    @abstractmethod
    def can_handle(self, message: str) -> bool:
        pass

    @abstractmethod
    async def handle(self, message: str, user_id: str) -> str:
        pass
