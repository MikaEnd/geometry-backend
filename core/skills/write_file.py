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
            "Без markdown, без пояснений, без форматирования. Без кода, который сам записывает файл."
        )

        response = ask_llm(system_prompt=system_prompt, user_message=message)
        raw = response.get("text", "").strip()

        print(f"🔍 Ответ от LLM:\n{raw}")

        # 💥 Частая ошибка — возврат кода, записывающего файл
        if "with open(" in raw and ".write(" in raw:
            retry_prompt = (
                "Ты помощник, который получает от пользователя имя файла и содержимое. "
                "Ответь строго:\n<имя файла>\n<содержимое файла>\nБез markdown, без пояснений, без кода, без Python."
            )
            retry = ask_llm(system_prompt=retry_prompt, user_message=message)
            raw = retry.get("text", "").strip()
            print(f"🔁 Перегенерация:\n{raw}")

        if not raw:
            return "⚠️ Ответ от LLM пустой."

        if "\n" not in raw:
            return f"⚠️ Не удалось извлечь имя и содержимое файла:\n{raw}"

        filename, content = raw.split("\n", 1)

        # Удаляем ```markdown```-обёртки
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
