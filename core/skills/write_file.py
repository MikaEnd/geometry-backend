from core.interfaces import Skill
from core.services.llm import ask_llm
import re

class WriteFileSkill(Skill):
    def can_handle(self, message: str) -> bool:
        return "сохрани" in message.lower() or "файл" in message.lower()

    async def execute(self, user_id: str, message: str) -> str:
        system_prompt = (
            "Ты файловый помощник. Получи от пользователя имя файла и его содержимое. "
            "Ответь строго в формате:\n<имя файла>\n<содержимое файла>. "
            "Без markdown, без пояснений, без форматирования. Без кода, который сам записывает файл."
        )

        response = ask_llm(system_prompt=system_prompt, user_message=message)
        raw = response.get("text", "").strip()

        print(f"🔍 Ответ от LLM:\n{raw}")

        if "with open(" in raw and ".write(" in raw:
            retry_prompt = (
                "Ответь строго в формате:\n<имя файла>\n<содержимое файла>.\n"
                "Без пояснений, без markdown, без кода, без Python. Только имя файла и его содержимое."
            )
            retry = ask_llm(system_prompt=retry_prompt, user_message=message)
            raw = retry.get("text", "").strip()
            print(f"🔁 Перегенерация:\n{raw}")

        raw = re.sub(r"^```(?:[a-z]+)?\n?", "", raw.strip(), flags=re.IGNORECASE)
        raw = re.sub(r"\n?```$", "", raw.strip())

        if not raw or "\n" not in raw:
            return f"⚠️ Не удалось извлечь имя и содержимое файла:\n{raw}"

        filename, content = raw.split("\n", 1)
        filename = filename.strip()
        content = content.strip()

        # ✅ Обновлённая валидация с поддержкой кириллицы
        if not re.match(r"^[\w\-.а-яА-ЯёЁ]+(\.py|\.txt|\.sh|\.md)?$", filename, re.IGNORECASE):
            return f"🚫 Недопустимое имя файла: {filename}"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            return f"📄 Файл {filename} успешно создан."
        except Exception as e:
            return f"🚫 Ошибка при записи файла: {e}"
