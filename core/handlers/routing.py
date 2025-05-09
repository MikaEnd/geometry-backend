# core/handlers/routing.py

from core.handlers.developer_handler import DeveloperHandler
from core.handlers.document_handler import DocumentHandler
from core.handlers.manager_handler import ManagerHandler

def get_handler_by_competence(competence: str):
    if "разработчик" in competence:
        return DeveloperHandler()
    elif "документ" in competence:
        return DocumentHandler()
    elif "менеджер" in competence:
        return ManagerHandler()
    elif "исследователь" in competence:
        # Пока заглушка — возвращает разработчика
        return DeveloperHandler()
    return None
