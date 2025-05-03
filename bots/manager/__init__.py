from core.base_handler import BaseHandler
from core.routing.llm_router import route_task
from core.skills.execute_with_llm import ExecuteWithLLMSkill
from core.services.ai_trace_logger import log_trace

class ManagerHandler(BaseHandler):
    def __init__(self):
        self.skill = ExecuteWithLLMSkill()

    async def handle(self, message: str, user_id: str) -> str:
        # Маршрутизация по смыслу
        routing_result = route_task(message)

        log_trace(
            user_id=user_id,
            message=message,
            mode="delegate",
            competence=routing_result.competence,
            handler=routing_result.handler_name
        )

        if routing_result.handler:
            return await routing_result.handler.handle(message, user_id)

        # Если не найдено — fallback на ExecuteWithLLMSkill
        if self.skill.can_handle(message):
            return await self.skill.execute(user_id, message)

        return "⚠️ Не удалось найти подходящего обработчика для задачи."
