# core/skills/self_heal_skill.py

from core.services.llm import ask_llm

class SelfHealSkill:
    @staticmethod
    def run(task: str, error: str = "") -> str:
        system_prompt = (
            "Ты инженер Python-системы с доступом к Ubuntu. "
            "Проанализируй проблему и предложи решение: что установить, изменить или перезапустить. "
            "Если ошибка от сервера (например, 403, 404), предложи альтернативу или способ обойти."
        )
        user_prompt = (
            f"Задача: {task}\n"
            f"Ошибка: {error}\n"
            "Что нужно сделать, чтобы задача могла быть выполнена?"
        )
        result = ask_llm(system_prompt, user_prompt)
        return result.get("text", "⚠️ Не удалось получить рекомендации.")
