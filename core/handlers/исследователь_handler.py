from core.handlers.base_handler import BaseHandler

class ИсследовательHandler(BaseHandler):
    async def handle(self, user_id: str, message: str) -> str:
        return f"🤖 Новый суб-бот ИсследовательHandler пока не реализован полностью. Задача: '{message}'"
