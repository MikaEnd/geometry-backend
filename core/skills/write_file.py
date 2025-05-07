from core.interfaces import Skill
from core.services.llm import ask_llm

class WriteFileSkill(Skill):
    def can_handle(self, message: str) -> bool:
        return "сохрани" in message or "файл" in message

    async def execute(self, user_id: str, message: str) -> str:
        system_prompt = (
            "Ты файловый помощник. Получи от пользователя имя файла и его содержимое. "
            "Ответь в формате: <filename>\n<content>. Без markdown, без пояснений."
        )
        response = ask_llm(system_prompt=system_prompt, user_message=message)
        raw = response.get("text", "").strip()

        if "\n" not in raw:
            return f"⚠️ Не удалось извлечь имя и содержимое файла: {raw}"

        filename, content = raw.split("\n", 1)
        try:
            with open(filename.strip(), "w", encoding="utf-8") as f:
                f.write(content.strip())
            return f"📄 Файл {filename.strip()} создан."
        except Exception as e:
            return f"🚫 Ошибка при записи файла: {e}"
