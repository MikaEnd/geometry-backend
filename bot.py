import asyncio
from bots.manager import ManagerHandler

def is_potential_command(text: str) -> bool:
    keywords = ["создай", "сохрани", "удали", "выполни", "сделай", "проверь", "напиши", "переведи", "перепиши"]
    return any(text.lower().strip().startswith(k) for k in keywords)

async def main():
    handler = ManagerHandler()
    while True:
        task = input("💬 Введите задачу: ").strip()
        if not task:
            continue

        if not is_potential_command(task):
            print("❓ Это:")
            print("1 → задача для исполнения")
            print("2 → просто вопрос (чат)")
            choice = input("Выберите (1/2): ").strip()
            if choice == "2":
                print("🤖 Ответ от ассистента:")
                print(handler.llm.ask_sync(task))
                continue
            elif choice != "1":
                print("❌ Ввод отменён.\n")
                continue

        result = await handler.handle("user-001", task)
        print(f"📎 Результат: {result}\n")

if __name__ == "__main__":
    asyncio.run(main())
