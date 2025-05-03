import os
import requests
import time
import sys
import tty
import termios
import fcntl
from core.skills.base_skill import BaseSkill
from core.services.command_executor import CommandExecutorService
from core.mediator.agent_mediator import delegate_task  # делегируем в менеджера

class ExecuteWithLLMSkill(BaseSkill):
    def __init__(self):
        self.executor = CommandExecutorService()

    def can_handle(self, message: str) -> bool:
        return any(x in message.lower() for x in [
            "установи", "удали", "обнови", "запусти", "создай", "bash", "терминал"
        ])

    async def execute(self, user_id: str, message: str) -> str:
        prompt = f"""Ты — помощник, превращающий задачи в bash-команды.
Преобразуй задачу: "{message}" в список bash-команд.
Если нужно создать многострочный текстовый файл — используй:
echo -e "строка1\\nстрока2" > путь/имя.txt
Не пиши Markdown, без пояснений. Только команды."""

        response = self.ask_llm(prompt)
        if "error" in response:
            return response["error"]

        raw_lines = response["text"].split("\n")
        commands = self.filter_commands(raw_lines)

        if not commands:
            return "⚠️ LLM не сгенерировал ни одной команды после фильтрации."

        print("\n🧾 Отфильтрованные команды:")
        for c in commands:
            print(f"  ⏳ Будет выполнено: {c}")

        print("\n⏱️ Выполнение начнётся через 9 секунд...")
        print("   ↩️ Нажмите Enter — чтобы выполнить немедленно.")
        print("   ␛  Нажмите Esc — чтобы отменить.")
        print("   ⏸️ Пробел — пауза / продолжить.\n")

        if not self.wait_for_confirmation():
            return "🚫 Пользователь отменил выполнение."

        results = []
        for cmd in commands:
            exec_result = self.executor.execute(cmd)
            output = exec_result["output"]
            status = "✅" if exec_result["status"] == "success" else "❌"
            results.append(f"{status} {cmd}\n{output}")

            if "command not found" in output:
                missing_command = cmd.split()[0]
                print(f"\n⚠️ Команда не найдена: {missing_command}")
                install_prompt = f"Установи утилиту {missing_command} в системе Ubuntu"
                install_result = await delegate_task("ExecuteWithLLMSkill", install_prompt, user_id)
                results.append(f"🔄 Установка {missing_command}: {install_result}")

        return f"📋 Задача: {message}\n" + "\n".join(results)

    def ask_llm(self, prompt: str) -> dict:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        api_url = os.getenv("DEEPSEEK_URL")
        if not api_key or not api_url:
            return {"error": "⛔️ Переменные окружения для LLM не заданы."}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"}
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2}
        try:
            res = requests.post(api_url, headers=headers, json=payload, timeout=20)
            res.raise_for_status()
            data = res.json()
            return {"text": data["choices"][0]["message"]["content"]}
        except Exception as e:
            return {"error": f"⚠️ Ошибка при обращении к LLM: {str(e)}"}

    def filter_commands(self, lines) -> list:
        filtered = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("```") or line.endswith("```"):
                continue
            if line.lower().startswith("bash"):
                continue
            filtered.append(line)
        return filtered

    def wait_for_confirmation(self) -> bool:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        tty.setcbreak(fd)
        fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)
        countdown = 9
        paused = False
        try:
            while countdown > 0:
                if not paused:
                    print(f"\r⌛ {countdown} ", end='', flush=True)
                    time.sleep(1)
                    countdown -= 1
                try:
                    key = os.read(fd, 1).decode()
                    if key == "\x1b":
                        print("\n🚫 Выполнение отменено пользователем.")
                        return False
                    elif key == "\n":
                        print("\n✅ Выполнение подтверждено.")
                        return True
                    elif key == " ":
                        paused = not paused
                        state = "⏸️ Пауза" if paused else "▶️ Продолжение"
                        print(f"\n{state}")
                except BlockingIOError:
                    continue
            print("\n⏳ Время истекло. Выполняем команды.")
            return True
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)
