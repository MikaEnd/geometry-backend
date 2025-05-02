from abc import ABC, abstractmethod

class SkillInterface(ABC):
    @abstractmethod
    def can_execute(self, task: str) -> bool:
        """
        Определяет, подходит ли навык для выполнения данной подзадачи.
        """
        pass

    @abstractmethod
    def execute(self, task: str) -> dict:
        """
        Выполняет задачу и возвращает результат.
        """
        pass
