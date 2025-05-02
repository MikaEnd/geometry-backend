import datetime
from core.handlers.manager_handler import ManagerHandler

LOG_FILE = "logs/AGENT_INTERACTION_LOG.txt"

async def delegate_to_another_agent(sender: str, user_id: str, task: str) -> str:
    timestamp = datetime.datetime.now().isoformat()

    try:
        result = await ManagerHandler().handle(user_id, task)
        log_entry = f"""### 🧩 Делегирование от {sender} → Manager
**⏱️ Время:** {timestamp}  
**📌 Задача:** {task}

**✅ Ответ:** {result}

---
"""
    except Exception as e:
        result = f"❌ Ошибка делегирования: {e}"
        log_entry = f"""### 🧩 Делегирование от {sender} → Manager
**⏱️ Время:** {timestamp}  
**📌 Задача:** {task}

**❌ Ошибка:** {e}

---
"""

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

    return result
