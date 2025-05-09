# core/skills/multi_step_task.py

from core.interfaces import Skill
from core.skills.execute_with_llm import ExecuteWithLLMSkill
from core.services.llm import ask_llm

class MultiStepTaskSkill(Skill):
    def can_handle(self, message: str) -> bool:
        return False  # вызывается вручную

    async def execute(self, user_id: str, message: str) -> str:
        prompt = f"Разбей задачу на bash-команды, которые нужно выполнить.\nЗадача: {message}"
        result = ask_llm("Ты умеешь декомпозировать задачи на шаги.", prompt)

        if result.get("error"):
            return f"⚠️ Ошибка LLM: {result['error']}"

        commands = result.get("text", "").strip().split("\n")
        handler = ExecuteWithLLMSkill()
        output = []

        for cmd in commands:
            if not cmd.strip():
                continue
            sub_message = f"{cmd.strip()}"
            out = await handler.execute(user_id, sub_message)
            output.append(out)

        return "\n\n".join(output)
