# MEMORY_README

Проект `geometry-backend` — это AI-система управления задачами, в которой центральный бот-координатор (ManagerHandler) получает пользовательские команды на естественном языке, определяет подходящую компетенцию и делегирует выполнение специальным суб-ботам.

## Основные компоненты:

- `bot.py` — основной скрипт запуска бота.
- `core/` — ядро системы: обработчики, навыки, маршрутизация.
- `bots/` — суб-боты по компетенциям:
  - `developer` — код, конфигурации, системы.
  - `web_researcher` — интернет-поиск.
  - `document` — работа с Word/docx.
  - `lawyer` — юридические проверки.
  - `llm_assistant` — fallback-бот для сложных задач.
- `memory/` — стратегическая документация и история изменений.

## Текущий статус

Система полностью очищена от жёсткой логики и ключевых слов. Все задачи обрабатываются через `llm_router` с fallback в ExecuteWithLLMSkill. Реализована поддержка паузы и отмены перед исполнением bash-команд.
