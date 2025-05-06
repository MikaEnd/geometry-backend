import re

# Паттерны команд, которые запрещено исполнять
DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/",            # Удаление корня
    r"\brm\s+-rf\b",            # rm -rf в любой форме
    r"\bshutdown\b",            # завершение работы
    r"\breboot\b",              # перезагрузка
    r"\bmkfs\.",                # форматирование
    r":\(\)\s*{\s*:\|\s*:;&\s*};",  # fork-бомба
    r"\bdd\s+if=",              # прямой доступ к устройствам
]

def sanitize_command(raw: str) -> str | None:
    """
    Очищает команду от Markdown-обрамлений и проверяет на опасность.
    Возвращает очищенную команду или None, если она заблокирована.
    """
    # Удалить обрамление ```bash и ```
    cleaned = raw.strip()
    cleaned = re.sub(r"^```bash\s*", "", cleaned)
    cleaned = re.sub(r"^```", "", cleaned)
    cleaned = re.sub(r"```$", "", cleaned)
    cleaned = cleaned.strip()

    # Проверка на опасные шаблоны
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, cleaned):
            return None

    return cleaned
