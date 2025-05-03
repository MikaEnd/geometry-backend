from pathlib import Path
from datetime import datetime

# Абсолютный путь к logs/AI_TRACE_LOG.md
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_PATH = BASE_DIR / "logs" / "AI_TRACE_LOG.md"

def log_trace(user_id: str, message: str, mode: str, competence: str | None, handler: str | None):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"""---
🕒 **{timestamp}**
👤 User: `{user_id}`
📝 Запрос: `{message}`
🔀 Режим: `{mode}`
🧠 Компетенция: `{competence or 'не определена'}`
🧩 Handler: `{handler or 'не найден'}`
"""
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry + "\n")
