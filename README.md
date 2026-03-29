[![Linter](https://github.com/Qusar0/detective-freelance-fastapi/actions/workflows/linter.yml/badge.svg)](https://github.com/Qusar0/detective-freelance-fastapi/actions/workflows/linter.yml)
[![Tests](https://github.com/Qusar0/detective-freelance-fastapi/actions/workflows/tests.yml/badge.svg)](https://github.com/Qusar0/detective-freelance-fastapi/actions/workflows/tests.yml)
# Detective Freelance

### Запуск проекта

1. Настройте виртуальное окружение проекта

```bash
cd ./server
python3.10 -m venv venv
source venv/bin/activate
python3.10 -m pip install -r requirements.txt
```

2. Создайте конфигурационный файл и запишите в него все настройки

```bash
cp .env.example .env
```

3. Проведите миграции через alembic

```bash
python -m alembic upgrade head
```

4. Выполните создание и поднятие контейнера проекта

```bash
sudo docker-compose up --build
```

Полезные ссылки:
- [Тестирование API](http://localhost:8001/docs)
- [Репозиторий клиента](https://github.com/Qusar0/ias_detective_frontend)

---

### Тесты
**Установка зависимостей для тестов:**

```bash
pip install pytest-asyncio==0.23.8 pytest-mock==3.14.0 freezegun==1.5.1
```

**Запуск всех тестов** (из корня репозитория):

```bash
pytest server/tests/ -v
```

**Только unit-тесты** (сервисы, декораторы - без HTTP):

```bash
pytest server/tests/unit/ -v
```

**Только интеграционные тесты** (роутеры через HTTP-клиент):

```bash
pytest server/tests/integration/ -v
```