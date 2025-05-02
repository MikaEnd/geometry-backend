import os
import requests
from core.interfaces import BotHandler

class LLMHandler(BotHandler):
    def can_handle(self, task_description: str) -> bool:
        return True  # сработает как универсальный fallback

    def handle(self, task_description: str) -> dict:
        api_key = os.getenv("LLM_API_KEY")
        url = os.getenv("LLM_API_URL")
        model = os.getenv("LLM_MODEL_NAME")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "Ты полезный AI-ассистент. Отвечай кратко, точно и в духе проекта."},
                {"role": "user", "content": task_description}
            ]
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=20)
            response.raise_for_status()
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            return {"result": f"🤖 Ответ от ассистента:\n{answer.strip()}"}
        except Exception as e:
            return {"error": f"⚠️ Ошибка при обращении к AI: {e}"}
