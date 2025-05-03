import os
from pathlib import Path

ROUTING_FILE = Path("core/handlers/routing.py")
TEMPLATE_HANDLER = '''from core.handlers.base_handler import BaseHandler

class {class_name}(BaseHandler):
    async def handle(self, user_id: str, message: str) -> str:
        return f"🤖 Новый суб-бот {class_name} пока не реализован полностью. Задача: '{{message}}'"
'''

def create_new_handler(competence: str) -> str:
    folder = competence.lower().replace(" ", "_")
    class_name = folder.capitalize() + "Handler"
    handler_file = Path(f"core/handlers/{folder}_handler.py")
    bot_folder = Path(f"bots/{folder}")
    bot_init = bot_folder / "__init__.py"

    # 1. bots/компетенция/__init__.py
    os.makedirs(bot_folder, exist_ok=True)
    if not bot_init.exists():
        bot_init.write_text("# init for " + folder)

    # 2. core/handlers/компетенция_handler.py
    if not handler_file.exists():
        handler_file.write_text(TEMPLATE_HANDLER.format(class_name=class_name))

    # 3. routing.py — добавить импорт и обработку
    with ROUTING_FILE.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    import_line = f"from core.handlers.{folder}_handler import {class_name}\n"
    handler_case = f"    elif \"{folder}\" in competence:\n        return {class_name}()\n"

    if import_line not in lines:
        for i, line in enumerate(lines):
            if line.startswith("def get_handler_by_competence"):
                lines.insert(i, import_line)
                break

    if handler_case not in lines:
        for i, line in enumerate(lines):
            if "return DeveloperHandler()" in line or "return None" in line:
                lines.insert(i, handler_case)
                break

    with ROUTING_FILE.open("w", encoding="utf-8") as f:
        f.writelines(lines)

    return f"✅ Компетенция '{competence}' добавлена. Handler: {class_name}"
