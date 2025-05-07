from core.interfaces import Skill
from core.services.llm import ask_llm
from core.utils.command_executor import execute_command
from core.utils.user_prompt import confirm_or_cancel
from core.utils.bash_sanitizer import sanitize_command
import re

class ExecuteWithLLMSkill(Skill):
    def can_handle(self, message: str) -> bool:
        return True

    async def execute(self, user_id: str, message: str) -> str:
        system_prompt = (
            "Ты помощник в терминале Linux. Преобразуй запрос пользователя "
            "в корректную bash-команду. Без пояснений, без markdown. Только одна команда."
        )

        response = ask_llm(system_prompt=system_prompt, user_message=message)
        if "error" in response:
            return f"⚠️ Ошибка от LLM:\n{response['error']}"

        command = response.get("text", "").strip()
        print(f"🔧 Сгенерировано LLM:\n{command}")

        if "\n" in command:
            retry_prompt = (
                "Ты снова помощник в терминале Linux. Только одна строка. "
                "Без пояснений. Только bash-команда. Без markdown, "
                "без текста. Повтори задачу корректно."
            )
            retry = ask_llm(system_prompt=retry_prompt, user_message=message)
            command = retry.get("text", "").strip()
            print(f"🔁 Перегенерировано LLM:\n{command}")

        if not command:
            return "⚠️ LLM не сгенерировал команду."

        # 🛡️ Блокируем очевидные текстовые ответы
        if re.search(r"[а-яА-ЯЁё]", command) or command.lower().startswith(("это", "команда", "запрос", "возможно", "уточните")):
            return f"⚠️ LLM вернул текст, а не команду:\n{command}"

        sanitized = sanitize_command(command)
        if sanitized is None:
            return "🚫 Команда заблокирована по соображениям безопасности."

        approved = confirm_or_cancel(sanitized)
        if not approved:
            return "❌ Выполнение отменено."

        result = execute_command(sanitized)
        if not result.strip():
            return (
                f"📋 Задача: {message}\n"
                f"✅ {sanitized}\n"
                f"⚠️ Команда выполнена, но ничего не вывела."
            )

        return f"📋 Задача: {message}\n✅ {sanitized}\n\n📤 Результат:\n{result}"
