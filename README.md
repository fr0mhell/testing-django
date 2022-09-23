# Django Examples

Django examples for Yandex Praktikum webinars.

## Реализуем фитнес-трекер на Django!

1. Создаем виртуальное окружение
2. Устанавливаем зависимости
    ```shell
    pip install -U pip pip-tools setuptools wheel
    pip install -r requirements.txt
    ```
3. Запускаем Джанго-проект
    ```shell
    cd fitness
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser --email root@root.ru --username root -v 3
    ```
    
4. Заполняем тестовыми данными. [Management команды в Django](https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/)
    ```shell
    python manage.py filldb
    ```

## Вебинар 4: Django ORM и формы

* [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) - показывает запросы к БД при обращении к Джанго-приложению.
* [django-extensions](https://django-extensions.readthedocs.io/en/latest/#:~:text=Django%20Extensions%20is%20a%20collection,admin%20extensions%20and%20much%20more.) - расширенные команды для Django, и много чего еще.
В том числе "Джанго-консоль на стероидах" `shell_plus`

Запускаем Django Shell-Plus в Jupyter:

```shell
python manage.py shell_plus --notebook
```

## Вебинар 5: Тестирование Django-приложения (и не только)

### 1. Тестируем проект Спринта 2

* [Виды тестирования](https://www.softwaretestinghelp.com/the-difference-between-unit-integration-and-functional-testing/)
* [Unit тесты на Python](https://realpython.com/python-testing/)

### 2. Ищем ошибку в проекте Спринта 2

* [Дебаггинг](https://machinelearningmastery.com/python-debugging-tools/)
* [Дебаггер в PyCharm](https://www.jetbrains.com/help/pycharm/part-1-debugging-python-code.html)
* [Дебаггер в VS Code](https://code.visualstudio.com/docs/python/debugging)

### 3. Тестируем и отлаживаемся

* [PyCharm, Django and debug](https://www.pragmaticlinux.com/2020/09/setup-and-debug-a-django-app-in-pycharm-community-edition/)
* [VS Code and Django debug](https://code.visualstudio.com/docs/python/tutorial-django)
