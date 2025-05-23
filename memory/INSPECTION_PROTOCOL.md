# INSPECTION PROTOCOL

Любая новая LLM-сессия или подключение ассистента к проекту должно начинаться с инспекции. Инспекция состоит из следующих шагов:

1. **Запрос подтверждения**: ассистент просит пользователя выполнить `sync_github.sh push` вручную и подтвердить.

2. **Анализ содержимого папки memory/**: 
   - MEMORY_README.txt — основной входной файл.
   - prompt_for_new_assistant.md — ключевой для загрузки контекста.
   - Все остальные файлы — стратегические, отражают живую эволюцию проекта.

3. **Сбор данных об архитектуре**: ассистент обязан сформировать для себя полное представление о проекте, компетенциях, суб-ботах и формате общения.

4. **Обязательное условие**: без инспекции память считается недействительной.

5. **По завершении** ассистент должен:
   - подтвердить успешную загрузку контекста,
   - готовность работать в текущем протоколе,
   - и указать последний шаг, описанный в DEV_PLAN.txt.
## Этап инспекции — май 2025

✅ Шаг 1 — Аудит структуры проекта и фиксация текущей архитектуры.  
✅ Шаг 2 — Удалены устаревшие компоненты: `telegram_bot/`, `__old__.py`, `guess_competence`.  
✅ Шаг 3 — Документация актуализирована, структура проекта приведена в порядок.
