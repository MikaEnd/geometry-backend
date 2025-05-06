from core.interfaces import Skill
from core.services.llm import ask_llm
from core.utils.command_executor import execute_command
from core.utils.user_prompt import confirm_or_cancel
from core.utils.bash_sanitizer import sanitize_command

class ExecuteWithLLMSkill(Skill):
    def can_handle(self, message: str) -> bool:
        return True

    async def execute(self, user_id: str, message: str) -> str:
        system_prompt = (
            "Ты помощник в терминале Linux. Преобразуй запрос пользователя "
            "в корректную bash-команду. Без пояснений, без markdown. Только одна команда."
        )
        response = ask_llm(system_prompt=system_prompt, user_message=message)
        command = response.get("text", "").strip()

        sanitized = sanitize_command(command)
        if sanitized is None:
            return "🚫 Команда заблокирована по соображениям безопасности."

        approved = confirm_or_cancel(sanitized)
        if not approved:
            return "❌ Выполнение отменено."

        result = execute_command(sanitized)
        return f"📋 Задача: {message}\n✅ {sanitized}\n\n{result}"
