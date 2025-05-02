from core.handlers.base_handler import BaseHandler
from core.skills.execute_with_llm import ExecuteWithLLMSkill
import os

class DocumentHandler(BaseHandler):
    async def handle(self, user_id: str, message: str) -> str:
        task_description = f"""
Ты должен выполнить следующую задачу: {message}

Убедись, что установлены пакеты:
- python-docx
- docxtpl
- language-tool-python
- libreoffice (если понадобится)

Если чего-то не хватает, сгенерируй bash-команды для установки и выполни их через DeveloperHandler.
После установки — повторно выполни начальную задачу.

Файлы находятся в директории /home/avipython/geometry-backend/KENT/
- Основной документ: Договор.docx
- Источник реквизитов: карточка компании.docx
"""

        executor = ExecuteWithLLMSkill()
        return await executor.run(user_id, task_description)
