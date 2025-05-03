from bots.manager import ManagerHandler

async def delegate_task(agent_name: str, task_text: str, user_id: str) -> str:
    manager = ManagerHandler()
    log_prefix = f"[agent_mediator] {agent_name} → Manager: {task_text}"
    print(log_prefix)
    try:
        result = await manager.handle(task_text, user_id)
        return result
    except Exception as e:
        return f"❌ Ошибка делегирования от {agent_name} → Manager: {str(e)}"
