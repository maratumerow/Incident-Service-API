#!/bin/bash
# ============================================================================
# СКРИПТ ДЛЯ УПРАВЛЕНИЯ PRE-COMMIT
# ============================================================================

set -e  # Остановка при ошибках

# Переход в корневую директорию проекта (на один уровень выше от scripts/)
cd "$(dirname "$0")/.."


# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода заголовков
print_header() {
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo
}

# Функция для проверки успешности выполнения
check_success() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
        exit 1
    fi
}

case "$1" in
    "install")
        print_header "УСТАНОВКА PRE-COMMIT HOOKS"
        cd ./ && uv run pre-commit install
        check_success "Pre-commit hooks установлены"
        ;;

    "run")
        print_header "ЗАПУСК ВСЕХ PRE-COMMIT ПРОВЕРОК"
        cd ./ && uv run pre-commit run --all-files
        check_success "Все проверки прошли успешно"
        ;;

    "ruff")
        print_header "ПРОВЕРКА И ИСПРАВЛЕНИЕ КОДА (RUFF)"
        cd ./ && uv run pre-commit run ruff --all-files
        check_success "Ruff проверка завершена"
        ;;

    "format")
        print_header "ФОРМАТИРОВАНИЕ КОДА"
        cd ./ && uv run pre-commit run ruff-format --all-files
        check_success "Код отформатирован"
        ;;

    "mypy")
        print_header "ПРОВЕРКА ТИПОВ (MYPY)"
        cd ./ && uv run pre-commit run mypy --all-files
        check_success "MyPy проверка завершена"
        ;;

    "update")
        print_header "ОБНОВЛЕНИЕ PRE-COMMIT HOOKS"
        cd ./ && uv run pre-commit autoupdate
        check_success "Hooks обновлены"
        ;;

    "clean")
        print_header "ОЧИСТКА PRE-COMMIT КЭША"
        cd ./ && uv run pre-commit clean
        check_success "Кэш очищен"
        ;;

    *)
        echo -e "${YELLOW}Использование: ./scripts/precommit.sh [команда]${NC}"
        echo
        echo "Доступные команды:"
        echo -e "  ${GREEN}install${NC}  - Установить pre-commit hooks"
        echo -e "  ${GREEN}run${NC}      - Запустить все проверки"
        echo -e "  ${GREEN}ruff${NC}     - Проверить код с Ruff"
        echo -e "  ${GREEN}format${NC}   - Отформатировать код"
        echo -e "  ${GREEN}mypy${NC}     - Проверить типы с MyPy"
        echo -e "  ${GREEN}update${NC}   - Обновить hooks"
        echo -e "  ${GREEN}clean${NC}    - Очистить кэш"
        ;;
esac
