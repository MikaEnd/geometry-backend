from core.interfaces import Handler
from core.skills.generate_code import GenerateCodeSkill
from core.skills.write_file import WriteFileSkill

class DeveloperHandler(Handler):
    def __init__(self):
        self.skills = [
            GenerateCodeSkill(),
            WriteFileSkill(),
        ]
