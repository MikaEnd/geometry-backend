#!/bin/bash

echo "📁 Рабочая директория: $(pwd)"

if [ ! -d .git ]; then
  echo "❌ Текущая директория не является git-репозиторием: $(pwd)"
  exit 1
fi

echo "1 → Pull с GitHub (перезаписать локальную папку)"
echo "2 → Push на GitHub (отправить изменения)"
read -p "Выберите действие (1/2): " action

if [ "$action" == "1" ]; then
  git fetch origin main
  git reset --hard origin/main
elif [ "$action" == "2" ]; then
  git add .
  git commit -m "Automatic sync $(date '+%Y-%m-%d %H:%M:%S')" || echo "ℹ️ Нет изменений для коммита."
  git push origin main
else
  echo "❌ Неизвестная команда."
fi
