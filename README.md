# testing-django
Тестирование Django-приложения (и не только)

## 1. Тестируем проект Спринта 2

## 2. Ищем ошибку в проекте Спринта 2

* [Дебаггинг]()
* [Дебаггер в PyCharm]()
* [Дебаггер в VS Code]()

## 3. Реализуем фитнес-трекер на Django!

Стартуем проект

```shell
cd fitness
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --email root@root.ru --username root -v 3
```

Заполняем тестовыми данными. [Management команды в Django](https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/)

```shell
python manage.py filldb
```