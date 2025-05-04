from core.interfaces import BotHandler
from core.routing.llm_router import route_task
from core.skills.execute_with_llm import ExecuteWithLLMSkill
from core.services.ai_trace_logger import log_trace

class ManagerHandler(BotHandler):
    def __init__(self):
        self.fallback = ExecuteWithLLMSkill()

    async def handle(self, message: str, user_id: str) -> str:
        routing = route_task(message)

        log_trace(
            user_id=user_id,
            message=message,
            mode="delegate",
            competence=routing.competence,
            handler=routing.handler_name
        )

        if routing.handler:
            return await routing.handler.handle(message, user_id)

        if self.fallback.can_handle(message):
            return await self.fallback.execute(user_id, message)

        return "⚠️ Не удалось определить исполнителя и fallback не применим."
