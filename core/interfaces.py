from abc import ABC, abstractmethod

# 🔧 Интерфейс для навыков
class Skill(ABC):
    @abstractmethod
    def can_handle(self, message: str) -> bool:
        """Определяет, может ли навык обработать сообщение"""
        pass

    @abstractmethod
    async def execute(self, user_id: str, message: str) -> str:
        """Асинхронно выполняет задачу и возвращает результат"""
        pass

# 🔧 Интерфейс и реализация маршрутизатора задач
class BotHandler(ABC):
    @abstractmethod
    def can_handle(self, task_description: str) -> bool:
        pass

    @abstractmethod
    def handle(self, task_description: str) -> dict:
        pass

class TaskRouter:
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler: BotHandler):
        self.handlers.append(handler)

    def route(self, task_description: str):
        for handler in self.handlers:
            if handler.can_handle(task_description):
                return handler.handle(task_description)
