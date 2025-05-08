import asyncio
from core.handlers.manager_handler import ManagerHandler
from core.services.llm import ask_llm

async def main():
    handler = ManagerHandler()

    while True:
        task = input("💬 Введите задачу: ").strip()

        if not task:
            continue

        if "?" in task or task.lower().startswith(("что", "как", "почему", "зачем", "когда")):
            print("❓ Это:")
            print("1 → задача для исполнения")
            print("2 → просто вопрос (чат)")
            choice = input("Выберите (1/2): ").strip()

            if choice == "2":
                print("🤖 Ответ от ассистента:")
                response = ask_llm(system_prompt="Ты ассистент, кратко и точно отвечай на вопросы.", user_message=task)
                print(response)
                continue

        result = await handler.handle(user_id="anonymous", message=task)
        print("📎 Результат:", result)

if __name__ == "__main__":
    asyncio.run(main())
