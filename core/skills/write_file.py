from core.interfaces import Skill
from core.services.llm import ask_llm
import re

class WriteFileSkill(Skill):
    def can_handle(self, message: str) -> bool:
        return "сохрани" in message or "файл" in message

    async def execute(self, user_id: str, message: str) -> str:
        system_prompt = (
            "Ты файловый помощник. Получи от пользователя имя файла и его содержимое. "
            "Ответь строго в формате:\n<имя файла>\n<содержимое файла>. "
            "Без markdown, без пояснений, без форматирования."
        )
        response = ask_llm(system_prompt=system_prompt, user_message=message)
        raw = response.get("text", "").strip()

        if "\n" not in raw:
            return f"⚠️ Не удалось извлечь имя и содержимое файла:\n{raw}"

        filename, content = raw.split("\n", 1)

        # Удаляем обёртку ```python ... ``` если она есть
        content = re.sub(r"^```(?:python)?\n?", "", content.strip(), flags=re.IGNORECASE)
        content = re.sub(r"\n?```$", "", content.strip())

        try:
            with open(filename.strip(), "w", encoding="utf-8") as f:
                f.write(content.strip())
            return f"📄 Файл {filename.strip()} успешно создан."
        except Exception as e:
            return f"🚫 Ошибка при записи файла: {e}"
