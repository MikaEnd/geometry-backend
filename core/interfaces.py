from abc import ABC, abstractmethod

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
        return {"error": "❌ Подходящий исполнитель не найден"}
