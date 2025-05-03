import asyncio
from core.interfaces import TaskRouter
from bots.developer import DeveloperHandler
from bots.lawyer import LawyerHandler
from bots.web_researcher import WebResearcherHandler
from bots.llm_assistant import LLMHandler
from bots.manager import ManagerHandler  # ⬅️ только последним!

async def main():
    router = TaskRouter()
    router.add_handler(DeveloperHandler())
    router.add_handler(LawyerHandler())
    router.add_handler(WebResearcherHandler())
    router.add_handler(LLMHandler())        # ⬅️ до менеджера!
    router.add_handler(ManagerHandler())    # ⬅️ fallback — в самом конце

    print("🤖 Bot Coordinator запущен.\n")
    while True:
        task = input("💬 Введите задачу: ")
        result = router.route(task)
        if asyncio.iscoroutine(result):
            result = await result
        print(f"📎 Результат: {result}\n")

if __name__ == "__main__":
    asyncio.run(main())
