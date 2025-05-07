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

        # 🔍 Отладочный вывод — покажем весь ответ от LLM
        print(f"🔍 Ответ от LLM:\n{raw}")

        if not raw:
            return "⚠️ Ответ от LLM пустой."

        if "\n" not in raw:
            return f"⚠️ Не удалось извлечь имя и содержимое файла:\n{raw}"

        filename, content = raw.split("\n", 1)

        # Удаляем обёртку ```python ... ``` если есть
        content = re.sub(r"^```(?:python)?\n?", "", content.strip(), flags=re.IGNORECASE)
        content = re.sub(r"\n?```$", "", content.strip())

        filename = filename.strip()
        if not filename or not content:
            return f"⚠️ Некорректные данные:\nИмя файла: {filename}\nСодержимое:\n{content}"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            return f"📄 Файл {filename} успешно создан."
        except Exception as e:
            return f"🚫 Ошибка при записи файла: {e}"
