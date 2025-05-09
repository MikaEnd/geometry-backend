# core/skills/execute_with_llm.py

import subprocess
import asyncio
from core.skills.base_skill import BaseSkill
from core.utils.helpers import countdown_with_control
from core.skills.self_heal_skill import SelfHealSkill
from core.services.llm import ask_llm

class ExecuteWithLLMSkill(BaseSkill):
    def can_handle(self, message: str) -> bool:
        return True

    async def execute(self, user_id: str, task: str) -> str:
        bash_command = self.generate_command(task)

        print(f"🧾 Команда для выполнения: {bash_command}")
        await countdown_with_control()

        try:
            result = subprocess.run(
                bash_command,
                shell=True,
                check=True,
                text=True,
                capture_output=True,
                timeout=20
            )
            output = result.stdout.strip()
            return f"📋 Задача: {task}\n✅ {bash_command}\n📤 Результат:\n{output or '⚠️ Команда выполнена, но ничего не вывела.'}"
        except subprocess.CalledProcessError as e:
            suggestion = SelfHealSkill.run(task, e.stderr)
            return f"❌ Ошибка при выполнении:\n{e.stderr}\n🤖 Рекомендация:\n{suggestion}"
        except Exception as e:
            return f"⚠️ Непредвиденная ошибка: {str(e)}"

    def generate_command(self, task: str) -> str:
        system_prompt = (
            "Ты помощник в терминале Linux. Преобразуй запрос пользователя "
            "в одну валидную bash-команду. Без пояснений, без markdown. Только команда."
        )
        result = ask_llm(system_prompt, task)
        return result.get("text", "").strip()
