<h1 align="center"><a target="_blank" href="">Тестовое задание для РусГидро</a></h1>


### Стек:
![Python](https://img.shields.io/badge/Python-171515?style=flat-square&logo=Python)![3.11](https://img.shields.io/badge/3.11-blue?style=flat-square&logo=3.11)
![Django](https://img.shields.io/badge/Django-171515?style=flat-square&logo=Django)![4.1.7](https://img.shields.io/badge/4.1.7-blue?style=flat-square&logo=4.1.7)

### Задание
#### Вам необходимо разработать сервис, проверяющий корректность исчисления НДФЛ сотрудникам. 
#### ТЗ:
- Сделать веб-приложение на Flask/Django, с помощью которого пользователь может отправить файл с исходными данными и в ответ получить сформированный отчет, основанный на исходных данных;
- Разработать алгоритм создания отчета в виде Excel файла с заданной шапкой таблицы (файл «Шапка отчета.xlsx»);
- Отчет должен содержать следующие столбцы:
- - Филиал (из исходных данных)
- - Сотрудник (из исходных данных)
- - Налоговая база (из исходных данных)
- - Исчислено всего (из исходных данных)
- - Исчислено всего по формуле (новый столбец)
- - Отклонения (новый столбец) – если отклонений нет, то фон ячеек зеленый, иначе – красный
- Формула новых столбцов:
- - Исчислено всего по формуле – если «Налоговая база» < 5000000, то «Налоговая база» * 13%, иначе «Налоговая база» * 15%
- - Отклонения (новый столбец) – «Исчислено всего» - «Исчислено всего по формуле»
- Отчет должен быть отсортирован по убыванию по столбцу «Отклонения»
- В отчете должны быть только значения, формул для столбцов быть не должно.
- Из файла с исходными данными необходимо парсить только те столбцы, что указаны в 3 пункте с пометкой «из исходных данных».



### Маршруты
| Название | Метод | Описание | Авторизация |
|----------|-------|----------|-------------|
| documents/ | GET/POST | Загрузить и получить документ | Нет


### Запуск проекта
Клонируем репозиторий и переходим в него:
```bash
gh clone https://github.com/PivnoyFei/task_for_rus_hydro.git
cd task_for_rus_hydro
```

#### Открываем в консоли папку backend:
```bash
cd backend
```
#### Ставим зависимости из poetry.toml:
```bash
poetry install
```
#### Примените миграции:
```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate --noinput
```
#### Создайте суперпользователя Django:
```bash
poetry run python manage.py createsuperuser
```
#### Запускаем сервер:
```bash
poetry run python manage.py runserver
```

#### Теперь сервер доступен по адресу - http://localhost:8000

### Вариант с pip:
#### Создаем и активируем виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
```
#### для Windows
```bash
python -m venv venv
source venv/Scripts/activate
```
#### Открываем в консоли папку backend:
```bash
cd backend
```
#### Обновиляем pip и ставим зависимости из requirements.txt:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
#### Запускаем сервер:
```bash
python manage.py runserver
```

#### Автор
[Смелов Илья](https://github.com/PivnoyFei)
