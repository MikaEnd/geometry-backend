from core.interfaces import BotHandler

class LawyerHandler(BotHandler):
    def can_handle(self, task_description: str) -> bool:
        keywords = [
            "договор", "контракт", "юрист", "закон", "право",
            "статья", "юридичес", "суд", "ответственность", "исковое"
        ]
        return any(word in task_description.lower() for word in keywords)

    def handle(self, task_description: str) -> dict:
        return {
            "result": f"⚖️ Юрист приступает к задаче: {task_description}",
            "next": "📄 Пожалуйста, уточните тип документа или правовую ситуацию, чтобы я мог помочь более точно."
        }
