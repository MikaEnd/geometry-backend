from core.handlers.base_handler import BaseHandler
from core.skills.execute_with_llm import ExecuteWithLLMSkill

class DeveloperHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.skills = [
            ExecuteWithLLMSkill()
        ]
