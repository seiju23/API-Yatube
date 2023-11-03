### Yatube API
Это API для проекта Yatube. С помощью него Вы можете:
- Просматривать и создавать посты;
- Редактировать и удалять свои посты;
- Подписываться на интересных Вам авторов;
- Оставлять комментарии к публикациям.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/seiju23/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Стек технологий:
- Python
- DRF
- SQLite

## Об авторе:
Игорь Равлис (tg: @seiju23, email: seiju.pioneer23@gmail.com)
