# GitHub Actions CI/CD Pipeline

## Обзор

Этот workflow автоматизирует процесс проверки кода, тестирования и развертывания приложения.

## Структура Pipeline

### 📋 Job 1: Lint (Проверка кода)

**Триггеры:** Push и PR в ветки `main`, `develop`

**Шаги:**
- ✅ Проверка кода с помощью **Ruff** (линтер)
- ✅ Проверка форматирования кода **Ruff format**
- ✅ Проверка типов с помощью **MyPy**

### 🧪 Job 2: Test (Тестирование)

**Триггеры:** Push и PR в ветки `main`, `develop`

**Шаги:**
- ✅ Запуск всех тестов
- ✅ Сбор покрытия кода (coverage)
- ✅ Отправка отчета в Codecov (опционально)

### 🐳 Job 3: Build and Push (Сборка Docker образа)

**Триггеры:** Только при push в ветку `main` после успешного прохождения lint и test

**Шаги:**
- ✅ Сборка Docker образа
- ✅ Создание тегов (latest, sha, версия)
- ✅ Публикация в GitHub Container Registry (`ghcr.io`)
- ✅ Кэширование слоев для ускорения сборки

## Теги Docker образов

После успешного push в `main` создаются следующие теги:

- `ghcr.io/maratumerow/incident-service-api:latest` - последняя версия
- `ghcr.io/maratumerow/incident-service-api:main` - из ветки main
- `ghcr.io/maratumerow/incident-service-api:main-<sha>` - с хешем коммита

## Использование Docker образа

### Pull образа

```bash
docker pull ghcr.io/maratumerow/incident-service-api:latest
```

### Запуск контейнера

```bash
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db \
  ghcr.io/maratumerow/incident-service-api:latest
```

### С docker-compose

```yaml
services:
  app:
    image: ghcr.io/maratumerow/incident-service-api:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/incident_db
```

## Локальная проверка

Перед push можно запустить проверки локально:

```bash
# Линтер
uv run ruff check .

# Форматирование
uv run ruff format --check .

# MyPy
uv run mypy app/

# Тесты с покрытием
uv run pytest tests/ -v --cov=app --cov-report=term-missing
```

## Требования

- Python 3.11+
- uv package manager
- Docker (для сборки образов)
- GitHub токен с правами на packages (автоматически доступен в Actions)

## Troubleshooting

### Ошибка доступа к GHCR

Убедитесь, что в настройках репозитория:
- Settings → Actions → General → Workflow permissions
- Выбрано "Read and write permissions"

### Тесты не проходят локально

```bash
# Переустановите зависимости
uv sync --reinstall

# Проверьте версию Python
python --version  # Должна быть 3.11+
```
