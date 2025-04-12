# barterplatfrom
## Установка и запуск проекта

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/yourusername/barter-platform.git
cd barter-platform
```

### 2. Создайте виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Установите Django
```bash
pip install django
```

### 4. Примените миграции
```bash
python testproject\manage.py makemigrations
python testproject\manage.py migrate
```

### 5. Запустите сервер
```bash
python testproject\manage.py runserver #http://127.0.0.1:8000
```

### Запуск тестов
```bash
python testproject\manage.py test ads
```
