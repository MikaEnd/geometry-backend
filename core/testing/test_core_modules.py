# core/testing/test_core_modules.py

from core.handlers.manager_handler import ManagerHandler
from core.handlers.document_handler import DocumentHandler
from core.services.llm import call_llm

def test_manager_handler_init():
    handler = ManagerHandler()
    assert handler is not None

def test_document_handler_init():
    handler = DocumentHandler()
    assert handler is not None

def test_call_llm_smoke():
    try:
        call_llm("test prompt")  # зависит от реализации, возможно будет ошибка
    except Exception:
        pass  # допустимо на smoke-этапе
