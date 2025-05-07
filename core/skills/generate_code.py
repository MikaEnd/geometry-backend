from core.interfaces import Skill
from core.services.llm import ask_llm

class GenerateCodeSkill(Skill):
    def can_handle(self, message: str) -> bool:
        return "код" in message or "скрипт" in message

    async def execute(self, user_id: str, message: str) -> str:
        system_prompt = (
            "Ты помощник-программист. Сгенерируй корректный код по описанию. "
            "Не используй markdown, никаких пояснений — только код."
        )
        response = ask_llm(system_prompt=system_prompt, user_message=message)
        code = response.get("text", "").strip()

        if not code:
            return "⚠️ Не удалось сгенерировать код."
        return f"📋 Задача: {message}\n\n💻 Код:\n{code}"
