# Ассистент в путешествиях "Passepartout"
Одновременно пользоваться десятками различных приложений крайне неудобно, в "Passepartout" вы сможете загружать и отслеживать заказы и получать статистику поездок

## Содержание
- [Технологии](#ехнологии)
- [Функционал](#функционал)
- [Использование](#использование)
- [Тестирование](#тестирование)
- [Команда проекта](#команда-проекта)

## Технологии
- [Django](https://www.djangoproject.com//)
- [Docker](https://www.docker.com/)
- HTML
- JavaScript
- Python

## Функционал
1. Создание аккаунта в общей системе
2. Загрузка своих билетов в формате .pdf для учёта их в статистике
3. Статистика аккаунта включает в себя: количество посещенных стран и предстоящих поездок, цену поездок в текущем месяце и длительность поездки
4. Уведомления на почту об изменениях в поездке(перенос/отмена рейса)
5. Система выдачи достижений на основе данных аккаунта
6. Соревнование между пользователями(в процессе разработки)

## Использование
1. Склонировать репозиторий и перейти в него:
```sh
git clone https://github.com/Ranger0806/
```
2. Далее установить необходимые библиотеки:
```
pip install -requirements.txt
```
3. Осуществить миграции
```
python manage.py migrate
```
4. Запустить проект

## Тестирование
```
from django.test import TestCase

from firstapp.models import ProjectUser
from firstapp.managers import CustomUserManager

class managerTestCase(TestCase):
def authenticationTest(self):
pass

    def resigterTest(self):
        pass

    def registerProcessTest(self):
        pass

    def authorizationTest(self):
        pass

    def authentication_process_Test(self):
        pass


class modelsTestCase(TestCase):
pass
```

## Команда проекта

- Нечаев Антон - Fullstack-разработчик
- Насуханов Муслим - Backend-разработчик
- Сеничев Герман - Создатель презентации
- Гуков Ярослав - DevOps
###### 
Данные учетной записи для быстрого доступа к сайту:'добавить потом'
