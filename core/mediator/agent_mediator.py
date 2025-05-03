async def delegate_task(agent_name: str, task_text: str, user_id: str) -> str:
    print(f"[agent_mediator] {agent_name} → Manager: {task_text}")
    try:
        # ленивый импорт — прямо внутри функции, чтобы избежать круговой зависимости
        from bots.manager import ManagerHandler

        manager = ManagerHandler()
        result = await manager.handle(task_text, user_id)
        return result
    except Exception as e:
        return f"❌ Ошибка делегирования от {agent_name} → Manager: {str(e)}"
