import os
import requests

def ask_llm(system_prompt: str, user_message: str) -> dict:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    api_url = os.getenv("DEEPSEEK_URL")

    if not api_key or not api_url:
        return {"error": "⛔️ Переменные окружения для LLM не заданы."}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.2
    }

    try:
        res = requests.post(api_url, headers=headers, json=payload, timeout=20)
        res.raise_for_status()
        data = res.json()
        return {"text": data["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": f"⚠️ Ошибка при обращении к LLM: {str(e)}"}
