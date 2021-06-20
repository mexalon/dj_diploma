# Для запуска проекта необходимо:

Установить зависимости:

```bash
pip install -r requirements.txt
```

создать базу в postgres и прогнать миграции:

```base
manage.py migrate
```

Выполнить команду:

```bash
python manage.py runserver
```

Примеры http запросов в файле 
```bash
requests-examples.http
```