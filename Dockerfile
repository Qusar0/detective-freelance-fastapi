FROM python:3.10-slim

# Установка зависимостей для TDLib и системных пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    git \
    cmake \
    zlib1g-dev \
    libssl-dev \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app/server

# Установка зависимостей Python
COPY ./server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всех файлов проекта
COPY . .

# Настройка переменных окружения
ENV PYTHONPATH=/app
ENV C_FORCE_ROOT=1
ENV LD_LIBRARY_PATH=/app/server/api/scripts/tdlib_sources

# Создание необходимых директорий
RUN mkdir -p /app/server/api/scripts/BotDB

# Запуск FastAPI через uvicorn
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
