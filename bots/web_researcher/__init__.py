from core.interfaces import BotHandler

class WebResearcherHandler(BotHandler):
    def can_handle(self, task_description: str) -> bool:
        keywords = ["найди", "поиск", "расписание", "сайт", "веб", "интернет", "страница", "открой", "где", "что такое"]
        return any(word in task_description.lower() for word in keywords)

    def handle(self, task_description: str) -> dict:
        simulated_links = [
            f"https://example.com/search?q={task_description.replace(' ', '+')}",
            f"https://search.com/results?query={task_description.replace(' ', '+')}",
            f"https://infohub.net/find/{task_description.replace(' ', '-')}"
        ]
        return {
            "result": f"🌐 Найдено по запросу: «{task_description}»",
            "links": [f"🔗 {url}" for url in simulated_links]
        }
