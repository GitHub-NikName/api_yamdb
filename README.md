
# api_yamdb
api_yamdb

### Технологии
- Python 3.9
- Django 3.2
- DRF 3.12
- Docker


### Как запустить проект:
- Клонировать репозиторий и перейти в него в командной строке:
```bash
https://github.com/GitHub-NikName/api_yamdb/tree/develop
cd api_yamdb
```

```bash
docker-compose up -d
docker exec -it api_yamdb sh
python manage.py migrate
````

###
Или:
- создать и активировать виртуальное окружение:
```bash
python -m venv env
source env/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt  
```

- Если у вас Linux/macOS
```
source env/bin/activate
```

- Если у вас windows
```
source env/scripts/activate
```
###
- Выполнить миграции
- Запустить проект
```bash
python manage.py migrate
python manage.py runserver
```

#
### Загрузить в базу пользователей из static/data/users.csv
```bash
python manage.py load_users
```

### Контакты:

[//]: # (Михаил  )
[//]: # ([email]&#40;server-15@yandex.ru&#41;  )
[//]: # ([telegram]&#40;https://t.me/sergeev_mikhail&#41;)