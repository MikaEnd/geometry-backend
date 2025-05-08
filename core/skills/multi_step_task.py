from core.services.llm import ask_llm
from core.routing.llm_router import get_handler_by_competence

class MultiStepTaskSkill:
    def __init__(self):
        self.executed_results = []

    async def execute(self, user_id: str, complex_task: str) -> str:
        # 1. Запрос декомпозиции задачи
        prompt = (
            f"Раздели следующую задачу на логические шаги с краткими формулировками:\n"
            f"{complex_task}\n\n"
            f"Формат ответа:\n"
            f"1. шаг один\n"
            f"2. шаг два\n"
            f"..."
        )
        response = await ask_llm(system_prompt="Ты умеешь декомпозировать задачи на шаги.", user_message=prompt)
        steps = self._extract_steps(response)

        if not steps:
            return "Не удалось декомпозировать задачу."

        final_report = "🧩 Декомпозиция задачи выполнена:\n"
        for idx, step in enumerate(steps, start=1):
            final_report += f"\n🔹 Шаг {idx}: {step}"

            competence_prompt = (
                f"Определи, какой исполнитель лучше подойдёт для выполнения следующего шага:\n"
                f"{step}\nОтветь одним словом: разработчик, исследователь, менеджер или неизвестно."
            )
            competence = await ask_llm(system_prompt="Ты классификатор задач по компетенциям.", user_message=competence_prompt)
            handler = get_handler_by_competence(competence)

            if handler:
                try:
                    result = await handler.handle(user_id, step)
                    self.executed_results.append((step, result))
                    final_report += f"\n✅ Выполнено: {result}\n"
                except Exception as e:
                    final_report += f"\n⚠️ Ошибка при выполнении: {e}\n"
            else:
                final_report += f"\n❌ Не найден исполнитель с компетенцией: {competence}\n"

        return final_report

    def _extract_steps(self, raw: str) -> list[str]:
        lines = raw.strip().splitlines()
        steps = []
        for line in lines:
            if "." in line:
                step = line.split(".", 1)[1].strip()
                if step:
                    steps.append(step)
        return steps
