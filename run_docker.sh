#!/bin/bash

echo "🔥 Hot Wheels Monitor (Docker)"
echo "============================="
echo ""

if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "📋 Создаем из примера..."
    cp .env.example .env
    echo "✅ Создан файл .env - отредактируйте его!"
    echo ""
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    exit 1
fi

echo "✅ Все проверки пройдены"
echo ""
echo "🐳 Запуск Docker контейнера..."
echo ""

docker-compose up -d

echo ""
echo "✅ Контейнер запущен!"
echo "📊 Для просмотра логов используйте:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Для остановки используйте:"
echo "   docker-compose down"