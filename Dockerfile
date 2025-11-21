# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем curl для healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv для управления зависимостей
RUN pip install --no-cache-dir uv

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем только production зависимости
RUN uv sync --frozen --no-dev

# Копируем код приложения
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./

# Открываем порт приложения
EXPOSE 8000

# Команда запуска приложения
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
