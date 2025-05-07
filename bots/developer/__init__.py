from core.interfaces import BotHandler
from core.skills.generate_code import GenerateCodeSkill
from core.skills.write_file import WriteFileSkill

class DeveloperHandler(BotHandler):
    def __init__(self):
        self.skills = [
            GenerateCodeSkill(),
            WriteFileSkill(),
        ]
