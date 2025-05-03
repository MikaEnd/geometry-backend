from pathlib import Path
from datetime import datetime

LOG_FILE = Path("logs/AI_TRACE_LOG.md")

def log_trace(user_id: str, message: str, mode: str, competence: str, handler_name: str):
    timestamp = datetime.now().isoformat()
    log_entry = f"""### 🧠 AI Trace Log
**⏱ Время:** {timestamp}  
**👤 Пользователь:** {user_id}  
**📝 Задача:** {message}  
**🧩 Тип:** {mode}  
**📚 Компетенция:** {competence or "—"}  
**🤖 Handler:** {handler_name or "—"}  

---
"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
