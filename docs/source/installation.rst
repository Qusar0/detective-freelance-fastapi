Установка
=========


Создание виртуального окружения:

.. code-block:: bash

    cd ./server
    python3.10 -m venv venv
    source venv/bin/activate


Установка зависимостей:

.. code-block:: bash

    python3.10 -m pip install --upgrade pip
    python3.10 -m pip install -r requirements.txt


Создание конфигурационного файла:

.. code-block:: bash

    cp .env.example .env


Разворачивание контейнеров проекта

.. code-block:: bash

    docker compose up --build