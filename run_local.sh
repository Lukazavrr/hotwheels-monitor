#!/bin/bash

echo "🔥 Hot Wheels Monitor"
echo "====================="
echo ""

if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "📋 Создаем из примера..."
    cp .env.example .env
    echo "✅ Создан файл .env - отредактируйте его!"
    echo ""
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен!"
    exit 1
fi

echo "✅ Все проверки пройдены"
echo ""
echo "📦 Создание директорий..."
mkdir -p logs data

echo ""
echo "🚀 Запуск Hot Wheels Monitor..."
echo ""

python3 main.py