#!/bin/bash

# Получаем текущую директорию
LOCAL_DIR="$(pwd)"

# Проверим, является ли папка git-репозиторием
if [ ! -d "$LOCAL_DIR/.git" ]; then
    echo "❌ Текущая директория не является git-репозиторием: $LOCAL_DIR"
    exit 1
fi

echo "📁 Рабочая директория: $LOCAL_DIR"
echo "1 → Pull с GitHub (перезаписать локальную папку)"
echo "2 → Push на GitHub (отправить изменения)"
read -n 1 -p "Выберите действие (1/2): " choice
echo ""

case $choice in
    1)
        git fetch origin
        git reset --hard origin/main
        git clean -fd
        ;;
    2)
        git add .
        git commit -m "Automatic sync $(date +'%Y-%m-%d %H:%M:%S')"
        git push origin main
        ;;
    *)
        echo "❌ Отмена"
        ;;
esac
