#!/bin/bash
# ============================================================================
# ЛОКАЛЬНАЯ ПРОВЕРКА CI/CD PIPELINE
# ============================================================================
# Этот скрипт запускает все проверки, которые выполняются в GitHub Actions
# Используйте его перед push, чтобы убедиться, что код пройдет CI/CD

set -e  # Остановить при первой ошибке

echo "🔍 Запуск локальной проверки CI/CD..."
echo ""

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для печати статуса
print_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1${NC}"
    else
        echo -e "${RED}✗ $1${NC}"
        exit 1
    fi
}

# === LINT JOB ===
echo -e "${YELLOW}📝 LINT: Проверка качества кода${NC}"
echo "-----------------------------------"

echo "→ Запуск Ruff linter..."
uv run ruff check . --config tools/ruff.toml
print_status "Ruff linter"

echo "→ Проверка форматирования..."
uv run ruff format --check . --config tools/ruff.toml
print_status "Ruff formatter"

echo "→ Проверка типов MyPy..."
uv run mypy app/ --config-file tools/mypy.ini
print_status "MyPy type checker"

echo ""

# === TEST JOB ===
echo -e "${YELLOW}🧪 TEST: Запуск тестов${NC}"
echo "-----------------------------------"

echo "→ Запуск тестов с покрытием..."
uv run pytest tests/ -v --cov=app --cov-report=term --cov-report=xml
print_status "Tests"

echo ""

# === BUILD CHECK ===
echo -e "${YELLOW}🐳 BUILD: Проверка Docker сборки${NC}"
echo "-----------------------------------"

echo "→ Проверка Dockerfile..."
if [ -f "Dockerfile" ]; then
    echo -e "${GREEN}✓ Dockerfile существует${NC}"
else
    echo -e "${RED}✗ Dockerfile не найден${NC}"
    exit 1
fi

echo "→ Сборка Docker образа (тест)..."
if docker build -t incident-service:test . > /dev/null 2>&1; then
    print_status "Docker build"
else
    echo -e "${RED}✗ Docker build failed${NC}"
    echo "Попробуйте запустить: docker build -t incident-service:test ."
    exit 1
fi

echo ""

# === SUMMARY ===
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Все проверки CI/CD пройдены успешно!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Ваш код готов к отправке в репозиторий 🚀"
