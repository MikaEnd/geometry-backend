from core.interfaces import BotHandler
from core.skills.execute_with_llm import ExecuteWithLLMSkill

class DeveloperHandler(BotHandler):
    def __init__(self):
        self.llm_skill = ExecuteWithLLMSkill()

    def can_handle(self, task_description: str) -> bool:
        keywords = ["установи", "настрой", "docker", "nginx", "код", "создай", "скрипт", "init"]
        return any(word in task_description.lower() for word in keywords)

    def handle(self, task_description: str) -> dict:
        if self.llm_skill.can_execute(task_description):
            return self.llm_skill.execute(task_description)

        return {
            "result": f"💻 Разработчик приступает к задаче: {task_description}",
            "next": "🛠 Уточните, пожалуйста, язык, стек, цели и особенности — и я сгенерирую конфигурацию или код."
        }
