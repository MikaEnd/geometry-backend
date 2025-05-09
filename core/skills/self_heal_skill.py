# core/skills/self_heal_skill.py

from core.services.llm import ask_llm

class SelfHealSkill:
    @staticmethod
    def run(task: str) -> str:
        system_prompt = (
            "Ты инженер Python-системы с доступом к Ubuntu. "
            "Твоя задача — определить, почему команда не может быть выполнена, и что нужно для исправления. "
            "Предложи конкретные действия: какие библиотеки установить, какие модули добавить, какие ошибки устранить."
        )
        user_prompt = f"Система не справилась с задачей: {task}\nЧто нужно сделать, чтобы она могла её выполнить?"

        result = ask_llm(system_prompt, user_prompt)
        return result.get("text", "⚠️ Не удалось получить рекомендации.")
