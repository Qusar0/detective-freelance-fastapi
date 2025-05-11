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
cd ./server && touch .env
cp .env.example .env
```

3. Проведите миграции через alembic

```bash
python -m alembic upgrade head
```

4. Выполните создание и поднятие контейнера проекта

```bash
sudo docker-compose build
sudo docker-compose up
```

Для тестирования API перейдите по: http://localhost:8001/docs