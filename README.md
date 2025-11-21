# Incident Service API

[![CI/CD Pipeline](https://github.com/maratumerow/Incident-Service-API/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/maratumerow/Incident-Service-API/actions/workflows/ci-cd.yml)
[![codecov](https://codecov.io/gh/maratumerow/Incident-Service-API/branch/main/graph/badge.svg)](https://codecov.io/gh/maratumerow/Incident-Service-API)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

REST API сервис для учёта и управления инцидентами, построенный на FastAPI с использованием принципов **Clean Architecture** и **SOLID**.

## Содержание

- [Возможности](#возможности)
- [Технологии](#технологии)
- [Архитектура](#архитектура)
  - [Структура проекта](#структура-проекта)
  - [Принципы проектирования](#принципы-проектирования)
  - [Поток выполнения запроса](#поток-выполнения-запроса)
  - [Примеры кода](#примеры-кода)
- [Быстрый старт](#быстрый-старт)
- [Миграции базы данных](#миграции-базы-данных)
- [API Endpoints](#api-endpoints)
- [Разработка](#разработка)
- [Тестирование](#тестирование)
- [CI/CD](#cicd)

## Возможности

- ✅ **Создание инцидентов** с описанием, статусом и источником
- 📋 **Получение списка инцидентов** с фильтрацией по статусу
- 🔍 **Поиск инцидента** по ID
- 🔄 **Обновление статуса** инцидента
- 🗄️ **Хранение данных** в PostgreSQL с ACID гарантиями
- 🔒 **Unit of Work** паттерн для управления транзакциями
- 📚 **Автоматическая документация** API (Swagger/ReDoc)
- 🐳 **Docker & Docker Compose** поддержка
- 🔄 **Автоматические миграции** базы данных (Alembic)
- ✅ **Покрытие тестами** с использованием pytest
- 🚀 **CI/CD pipeline** с GitHub Actions
- 🏗️ **Clean Architecture** с разделением на слои
- 🎯 **SOLID принципы** и Domain-Driven Design

## Технологии

### Backend
- **Python 3.11+** - современная версия Python с улучшенной типизацией
- **FastAPI** - высокопроизводительный асинхронный веб-фреймворк
- **SQLAlchemy 2.0** - ORM с асинхронным режимом работы
- **PostgreSQL 15** - надёжная реляционная база данных
- **asyncpg** - высокопроизводительный асинхронный драйвер для PostgreSQL
- **Alembic** - управление миграциями базы данных
- **Pydantic 2.0** - валидация данных и настроек
- **uvicorn** - ASGI веб-сервер

### Инструменты разработки
- **uv** - быстрый менеджер зависимостей Python
- **Ruff** - современный линтер и форматтер (замена flake8, black, isort)
- **MyPy** - статическая проверка типов
- **Ty** - дополнительная проверка типов
- **pytest** - фреймворк для тестирования
- **pytest-asyncio** - асинхронные тесты
- **pytest-cov** - покрытие кода тестами
- **httpx** - HTTP клиент для тестирования API
- **pre-commit** - Git hooks для проверки кода перед коммитом

### DevOps
- **Docker & Docker Compose** - контейнеризация приложения
- **GitHub Actions** - CI/CD pipeline
- **Codecov** - отслеживание покрытия кода

## Архитектура

Проект реализован с использованием **Clean Architecture**, **Domain-Driven Design** паттернов и **полностью асинхронного программирования**.

### Структура проекта

```
app/
├── domain/              # 🎯 Доменный слой (бизнес-логика)
│   ├── entities.py      # Доменные сущности (Incident)
│   ├── enums.py         # Перечисления (IncidentStatus, IncidentSource)
│   ├── exceptions.py    # Доменные исключения (IncidentNotFoundError)
│   └── interfaces.py    # Абстракции/интерфейсы:
│                        #   - IIncidentRepository (репозиторий)
│                        #   - IUnitOfWork (управление транзакциями)
│
├── application/         # 💼 Слой приложения
│   └── use_cases.py     # Бизнес-логика (Use Cases):
│                        #   - CreateIncidentUseCase
│                        #   - GetIncidentsUseCase
│                        #   - GetIncidentByIdUseCase
│                        #   - UpdateIncidentStatusUseCase
│
├── infrastructure/      # 🔧 Инфраструктурный слой
│   ├── database.py      # Настройка асинхронной SQLAlchemy
│   ├── models.py        # ORM модели (IncidentModel)
│   ├── repository.py    # Реализация репозиториев (IncidentRepository)
│   └── unit_of_work.py  # Unit of Work (SQLAlchemyUnitOfWork)
│
├── presentation/        # 🌐 Слой представления (API)
│   ├── routes.py        # HTTP endpoints (FastAPI routes)
│   └── schemas.py       # Pydantic схемы запросов/ответов
│
├── config.py            # ⚙️ Конфигурация (настройки из .env)
├── dependencies.py      # 🔌 Dependency Injection контейнер
└── main.py              # 🚀 Точка входа приложения
```

### Принципы проектирования

#### Clean Architecture
- ✅ **Независимость от фреймворков** - бизнес-логика не зависит от FastAPI
- ✅ **Тестируемость** - каждый слой можно тестировать независимо
- ✅ **Независимость от БД** - легко заменить PostgreSQL на другую БД
- ✅ **Разделение ответственности** - каждый слой имеет чёткую задачу

#### SOLID
- **S**ingle Responsibility - каждый класс отвечает за одну вещь
- **O**pen/Closed - расширяемость через интерфейсы без изменения кода
- **L**iskov Substitution - использование абстракций (IIncidentRepository, IUnitOfWork)
- **I**nterface Segregation - узкие специализированные интерфейсы
- **D**ependency Inversion - зависимость от абстракций, а не от реализаций

#### Паттерны проектирования

##### Unit of Work (UoW)
Централизованное управление транзакциями базы данных:

```python
# Use Case управляет границами транзакции
async def execute(...):
    async with self.uow:  # Начало транзакции
        incident = await self.uow.incidents.create(...)
        # Автоматический commit при успехе
        # Автоматический rollback при ошибке
```

**Преимущества:**
- ✅ Атомарность операций - одна транзакция для всех изменений
- ✅ Явные границы транзакций - контроль на уровне use case
- ✅ Автоматический rollback при исключениях
- ✅ Упрощённое тестирование - мокирование UoW вместо session
- ✅ Готовность к масштабированию - легко добавить новые репозитории

##### Repository Pattern
Абстракция доступа к данным:
- Репозитории работают только с данными (без управления транзакциями)
- Использование `flush()` вместо `commit()` для синхронизации
- Преобразование между доменными сущностями и ORM моделями

#### Асинхронность
- **async/await** во всех слоях приложения
- **SQLAlchemy AsyncSession** - неблокирующие запросы к БД
- **asyncpg** - высокопроизводительный драйвер PostgreSQL
- **FastAPI** - нативная поддержка асинхронных endpoints

### Поток выполнения запроса

```
HTTP Request
    ↓
FastAPI Route (presentation/routes.py)
    ↓
Dependency Injection (dependencies.py)
    ↓
Use Case (application/use_cases.py)
    ↓
Unit of Work (infrastructure/unit_of_work.py)
    ↓
Repository (infrastructure/repository.py)
    ↓
Database (PostgreSQL)
```

**Пример создания инцидента:**

1. **Route** получает HTTP запрос
2. **DI** создаёт `UnitOfWork` и `UseCase`
3. **UseCase** начинает транзакцию через `async with uow:`
4. **Repository** добавляет данные и делает `flush()`
5. **UoW** делает `commit()` всех изменений
6. **Route** возвращает ответ клиенту

При ошибке на любом этапе - **автоматический rollback** всех изменений.

### Примеры кода

<details>
<summary>📝 Создание инцидента через Use Case</summary>

```python
# app/application/use_cases.py
class CreateIncidentUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(
        self, description: str, status: IncidentStatus, source: IncidentSource
    ) -> Incident:
        incident = Incident(
            id=None,
            description=description,
            status=status,
            source=source,
            created_at=datetime.now(UTC),
        )

        # Транзакция управляется UoW
        async with self.uow:
            return await self.uow.incidents.create(incident)
            # Автоматический commit при успехе
            # Автоматический rollback при исключении
```

</details>

<details>
<summary>🔧 Unit of Work управление транзакциями</summary>

```python
# app/infrastructure/unit_of_work.py
class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.incidents = IncidentRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()  # Ошибка → откат
        else:
            await self.commit()    # Успех → коммит

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
```

</details>

<details>
<summary>💾 Repository без управления транзакциями</summary>

```python
# app/infrastructure/repository.py
class IncidentRepository(IIncidentRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, incident: Incident) -> Incident:
        db_incident = IncidentModel(
            description=incident.description,
            status=incident.status.value,
            source=incident.source.value,
            created_at=incident.created_at,
        )
        self.db.add(db_incident)
        await self.db.flush()  # ← Не commit! Только синхронизация
        return self._to_entity(db_incident)
```

</details>

<details>
<summary>🔌 Dependency Injection</summary>

```python
# app/dependencies.py
async def get_uow(db: AsyncSession = Depends(get_db)) -> IUnitOfWork:
    return SQLAlchemyUnitOfWork(db)

def get_create_incident_use_case(
    uow: IUnitOfWork = Depends(get_uow),
) -> CreateIncidentUseCase:
    return CreateIncidentUseCase(uow)

# app/presentation/routes.py
@router.post("/incidents", status_code=201)
async def create_incident(
    request: IncidentCreateRequest,
    use_case: CreateIncidentUseCaseDep,  # ← Автоматическая инъекция
):
    incident = await use_case.execute(...)
    return IncidentResponse(...)
```

</details>

## Быстрый старт

### Docker Compose (рекомендуется)

```bash
# Клонировать репозиторий
git clone https://github.com/maratumerow/Incident-Service-API.git
cd Incident-Service-API

# Запустить PostgreSQL и сервис
docker-compose up -d
```

✅ **Готово!** Сервис доступен по адресу: http://localhost:8000

**Что происходит автоматически:**
1. ⬇️ Скачивается и запускается PostgreSQL 15
2. 🗄️ Создаётся база данных `incident_db`
3. 🔄 Применяются миграции Alembic
4. 🚀 Запускается FastAPI приложение на порту 8000

**Полезные команды Docker:**
```bash
# Просмотр логов
docker-compose logs -f incident-service

# Остановка
docker-compose down

# Полная очистка (включая БД)
docker-compose down -v

# Перезапуск после изменений
docker-compose build && docker-compose up -d
```

### Локальная установка

<details>
<summary>Развернуть инструкцию</summary>

#### Требования
- Python 3.11+
- PostgreSQL 15+
- uv

#### 1️⃣ Установите PostgreSQL

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### 2️⃣ Создайте базу данных

```bash
psql -U postgres -c "CREATE DATABASE incident_db;"
```

#### 3️⃣ Установите uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 4️⃣ Настройте проект

```bash
git clone https://github.com/maratumerow/Incident-Service-API.git
cd Incident-Service-API

# Создать .env файл
cp .env.example .env
# Отредактируйте .env и укажите DATABASE_URL
```

#### 5️⃣ Установите зависимости

```bash
uv sync
```

#### 6️⃣ Примените миграции

```bash
uv run alembic upgrade head
```

#### 7️⃣ Запустите сервер

```bash
uv run uvicorn app.main:app --reload
```

✅ Сервер доступен: http://127.0.0.1:8000

</details>

### 📚 Документация API

После запуска доступна автоматическая интерактивная документация:

- 📖 **Swagger UI**: http://localhost:8000/docs
- 📋 **ReDoc**: http://localhost:8000/redoc

## Миграции базы данных

Проект использует **Alembic** для управления схемой базы данных.

```bash
# Применить все миграции
uv run alembic upgrade head

# Откатить последнюю миграцию
uv run alembic downgrade -1

# Посмотреть текущую версию БД
uv run alembic current

# Создать новую миграцию (автогенерация из моделей)
uv run alembic revision --autogenerate -m "Описание изменений"
```

### Создание миграции - пример workflow

1. Изменить модель в `app/infrastructure/models.py`
2. Сгенерировать миграцию:
   ```bash
   uv run alembic revision --autogenerate -m "Add new column"
   ```
3. Проверить файл в `alembic/versions/`
4. Применить миграцию:
   ```bash
   uv run alembic upgrade head
   ```

## ⚙️ Переменные окружения

Создайте файл `.env` в корне проекта:

```bash
cp .env.example .env
```

**Содержимое `.env`:**

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/incident_db

# Application
DEBUG=False
```

| Параметр | Описание | Пример |
|----------|----------|--------|
| `DATABASE_URL` | Строка подключения к PostgreSQL | `postgresql+asyncpg://user:password@host:5432/db` |
| `DEBUG` | Режим отладки | `False` |

> **Примечание**: В Docker используйте `@postgres` вместо `@localhost` в `DATABASE_URL`

## API Endpoints

### 🏥 Health Check

#### `GET /`

Проверка работоспособности сервиса.

**Пример:**
```bash
curl http://localhost:8000/
```

**Ответ:**
```json
{
  "status": "ok",
  "message": "Incident Service is running"
}
```

---

### 📝 Создать инцидент

#### `POST /incidents`

Создание нового инцидента.

**Request Body:**
```json
{
  "description": "Сервер недоступен",
  "status": "открыт",
  "source": "monitoring"
}
```

**Допустимые значения:**
- `status`: `"открыт"`, `"в работе"`, `"закрыт"`
- `source`: `"operator"`, `"monitoring"`, `"partner"`

**Пример:**
```bash
curl -X POST http://localhost:8000/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Сервер недоступен",
    "status": "открыт",
    "source": "monitoring"
  }'
```

**Ответ (201 Created):**
```json
{
  "id": 1,
  "description": "Сервер недоступен",
  "status": "открыт",
  "source": "monitoring",
  "created_at": "2025-11-21T10:30:00.123456"
}
```

---

### 📋 Получить список инцидентов

#### `GET /incidents`

Получение списка всех инцидентов с опциональной фильтрацией по статусу.

**Query параметры:**
- `status` (опционально) - фильтр по статусу

**Примеры:**

Все инциденты:
```bash
curl http://localhost:8000/incidents
```

Фильтр по статусу:
```bash
curl -G http://localhost:8000/incidents --data-urlencode "status=открыт"
```

**Ответ (200 OK):**
```json
[
  {
    "id": 1,
    "description": "Сервер недоступен",
    "status": "открыт",
    "source": "monitoring",
    "created_at": "2025-11-21T10:30:00.123456"
  },
  {
    "id": 2,
    "description": "Ошибка авторизации",
    "status": "в работе",
    "source": "operator",
    "created_at": "2025-11-21T11:15:00.789012"
  }
]
```

---

### 🔍 Получить инцидент по ID

#### `GET /incidents/{id}`

Получение одного инцидента по его ID.

**Пример:**
```bash
curl http://localhost:8000/incidents/1
```

**Ответ (200 OK):**
```json
{
  "id": 1,
  "description": "Сервер недоступен",
  "status": "открыт",
  "source": "monitoring",
  "created_at": "2025-11-21T10:30:00.123456"
}
```

**Ошибка (404 Not Found):**
```json
{
  "detail": "Incident with id 999 not found"
}
```

---

### 🔄 Обновить статус инцидента

#### `PATCH /incidents/{id}/status`

Обновление статуса инцидента.

**Request Body:**
```json
{
  "status": "в работе"
}
```

**Пример:**
```bash
curl -X PATCH http://localhost:8000/incidents/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "в работе"}'
```

**Ответ (200 OK):**
```json
{
  "id": 1,
  "description": "Сервер недоступен",
  "status": "в работе",
  "source": "monitoring",
  "created_at": "2025-11-21T10:30:00.123456"
}
```

---

### 📊 Модель данных

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный идентификатор (автоинкремент) |
| `description` | String | Текстовое описание инцидента |
| `status` | Enum | Статус: "открыт", "в работе", "закрыт" |
| `source` | Enum | Источник: "operator", "monitoring", "partner" |
| `created_at` | DateTime | Время создания (UTC) |

---

## Разработка

### Запуск в режиме разработки

```bash
# С автоперезагрузкой при изменениях
uv run uvicorn app.main:app --reload --port 8000
```

### Проверка кода

Проект включает автоматические проверки качества кода:

```bash
# Полная проверка (форматирование, линтинг, типы)
./scripts/check_code.sh

# Только форматирование
uv run ruff format ./app --config tools/ruff.toml

# Только линтинг
uv run ruff check ./app --config tools/ruff.toml

# Только проверка типов
uv run mypy ./app --config-file tools/mypy.ini
```

### Pre-commit hooks

Проект использует pre-commit для автоматической проверки перед коммитом:

```bash
# Установить hooks
uv run pre-commit install

# Запустить вручную
uv run pre-commit run --all-files
```

## Тестирование

Проект покрыт **интеграционными тестами** с использованием in-memory SQLite базы данных.

### Запуск тестов

```bash
# Все тесты
uv run pytest tests/

# С подробным выводом
uv run pytest tests/ -v

# С покрытием кода
uv run pytest tests/ -v --cov=app --cov-report=term

# С HTML отчётом покрытия
uv run pytest tests/ --cov=app --cov-report=html
# Откройте htmlcov/index.html в браузере
```

### Структура тестов

```
tests/
├── conftest.py                      # Фикстуры (db_session, client, UoW override)
├── test_create_incident.py          # Тесты создания инцидента
├── test_get_incidents.py            # Тесты получения списка
├── test_get_incident_by_id.py       # Тесты получения по ID
└── test_update_incident_status.py   # Тесты обновления статуса
```

### Тестовая инфраструктура

- **In-memory SQLite** - быстрая база данных для тестов
- **AsyncClient** - тестирование HTTP endpoints
- **Dependency Override** - подмена UoW и session для изоляции тестов
- **pytest-asyncio** - поддержка асинхронных тестов
- **Fixtures** - переиспользуемые компоненты (session, client)

### Примеры тестов

**Тест создания инцидента:**
```python
async def test_create_incident_success(client: AsyncClient):
    response = await client.post("/incidents", json={
        "description": "Server is down",
        "status": "открыт",
        "source": "monitoring"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Server is down"
    assert "id" in data
```

**Тест с фильтрацией:**
```python
async def test_get_incidents_filtered_by_status(client: AsyncClient):
    # Создаём инциденты
    await client.post("/incidents", json={...})

    # Фильтруем по статусу
    response = await client.get("/incidents?status=открыт")
    assert all(inc["status"] == "открыт" for inc in response.json())
```

## CI/CD

Проект использует **GitHub Actions** для автоматической проверки кода и развёртывания.

### Pipeline этапы

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    Lint     │────▶│    Test     │────▶│   Build &   │
│             │     │             │     │    Push     │
│ - Ruff      │     │ - pytest    │     │             │
│ - MyPy      │     │ - coverage  │     │ - Docker    │
│             │     │ - codecov   │     │ - GHCR      │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Workflow файл

Конфигурация находится в `.github/workflows/ci-cd.yml`:

1. **Lint** - проверка кода с Ruff и MyPy
2. **Test** - запуск тестов и отправка покрытия в Codecov
3. **Build and Push** - сборка Docker образа и публикация в GitHub Container Registry

## 🛠 Инструменты

### Качество кода

- **Ruff** - быстрый линтер и форматтер (замена flake8, black, isort)
  - Настройка: `tools/ruff.toml`
  - Длина строки: 79 символов (PEP 8)
  - Поддержка кириллицы в комментариях

- **MyPy** - статическая проверка типов
  - Настройка: `tools/mypy.ini`
  - Строгий режим: включен
  - Плагины: Pydantic, SQLAlchemy

- **Ty** - дополнительная проверка типов
  - Настройка: `tools/ty.toml`

### Скрипты

- `scripts/check_code.sh` - полная проверка кода
- `scripts/precommit.sh` - pre-commit проверки
- `scripts/test_ci.sh` - запуск CI проверок локально

## 📝 Лицензия

MIT

## 👨‍💻 Автор

[Marat Umerov](https://github.com/maratumerow)
