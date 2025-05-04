from core.interfaces import BotHandler

class DocumentHandler(BotHandler):
    def can_handle(self, task: str) -> bool:
        return any(x in task.lower() for x in ["документ", ".docx", "word", "реквизит", "текст", "грамматика"])

    async def handle(self, task: str, user_id: str) -> str:
        return f"📄 DocumentHandler получил задачу: {task}\n(реализация обработки документов в разработке)"
