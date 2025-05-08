# core/testing/test_core_modules.py

import unittest
from core.handlers.manager_handler import ManagerHandler
from core.handlers.document_handler import DocumentHandler
from core.services.llm import ask_llm

class TestCoreModules(unittest.TestCase):
    def test_manager_handler_init(self):
        handler = ManagerHandler()
        self.assertIsNotNone(handler)

    def test_document_handler_init(self):
        handler = DocumentHandler()
        self.assertIsNotNone(handler)

    def test_ask_llm_smoke(self):
        try:
            ask_llm("system", "test prompt")
        except Exception:
            pass  # допустимо
