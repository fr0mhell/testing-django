# testing-django

Тестирование Django-приложения (и не только)

## 1. Тестируем проект Спринта 2

* [Виды тестирования](https://www.softwaretestinghelp.com/the-difference-between-unit-integration-and-functional-testing/)
* [Unit тесты на Python](https://realpython.com/python-testing/)

## 2. Ищем ошибку в проекте Спринта 2

* [Дебаггинг](https://machinelearningmastery.com/python-debugging-tools/)
* [Дебаггер в PyCharm](https://www.jetbrains.com/help/pycharm/part-1-debugging-python-code.html)
* [Дебаггер в VS Code](https://code.visualstudio.com/docs/python/debugging)

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

## 4. Тестируем и отлаживаемся

* [PyCharm, Django and debug](https://www.pragmaticlinux.com/2020/09/setup-and-debug-a-django-app-in-pycharm-community-edition/)
* [VS Code and Django debug](https://code.visualstudio.com/docs/python/tutorial-django)
