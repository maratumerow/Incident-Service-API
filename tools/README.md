# 🔧 Tools Configuration

Эта папка содержит конфигурационные файлы для инструментов анализа кода.

## 📁 Структура

| Файл | Инструмент | Назначение |
|------|------------|------------|
| `ruff.toml` | [Ruff](https://docs.astral.sh/ruff/) | Линтинг и форматирование Python кода |
| `mypy.ini` | [MyPy](https://mypy.readthedocs.io/) | Статическая проверка типов |
| `ty.toml` | [Ty](https://github.com/astral-sh/ty) | Альтернативная быстрая проверка типов |

## 🚀 Использование

Все инструменты автоматически используют эти конфигурации через:

- **Скрипт проверки**: `./scripts/check_code.sh`
- **Pre-commit hooks**: `.pre-commit-config.yaml`
- **Ручные команды**:
  ```bash
  # Ruff
  uv run ruff check app/ --config tools/ruff.toml
  uv run ruff format app/ --config tools/ruff.toml

  # MyPy
  uv run mypy app/ --config-file tools/mypy.ini

  # Ty
  uv run ty check app/ --config-file tools/ty.toml
  ```
