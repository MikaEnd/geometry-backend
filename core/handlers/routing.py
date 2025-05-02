from core.handlers.manager_handler import ManagerHandler
from core.handlers.developer_handler import DeveloperHandler
# В будущем: from core.handlers.web_researcher_handler import WebResearcherHandler

def get_handler_by_competence(competence: str):
    competence = competence.lower()
    if "разработчик" in competence:
        return DeveloperHandler()
    elif "менеджер" in competence:
        return ManagerHandler()
    # elif "исследователь" in competence:
    #     return WebResearcherHandler()
    return None
