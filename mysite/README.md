# Simple Online Store

Цей проект - простий інтернет-магазин, реалізований з використанням Django. Він дозволяє користувачам переглядати товари та робити замовлення.

## Початок роботи

Перед тим, як запустити проект, вам потрібно встановити необхідні залежності та налаштувати базу даних.

### Вимоги

- Python 3.8 або новіше
- pip (Python package installer)
- Virtualenv (опційно)

### Встановлення

1. Клонуйте репозиторій:

```shell
git clone https://example.com/simple-online-store.git cd simple-online-store
```

2. Встановіть `virtualenv`, якщо ще не встановлений:

```shell
pip install virtualenv

```

3. Створіть та активуйте віртуальне середовище:

```shell
virtualenv venv source venv/bin/activate 
venv\Scripts\activate

```

4. Встановіть залежності:

```shell
pip install -r requirements.txt

```

### Налаштування бази даних

1. Створіть файл `.env` в корені проекту для зберігання секретних змінних:

SECRET_KEY='your_secret_key' DEBUG=True DB_NAME='dbname' DB_USER='dbuser' DB_PASSWORD='dbpassword' DB_HOST='localhost' DB_PORT='5432'

2. Запустіть міграції для створення таблиць у базі даних:

```shell
python manage.py migrate
```



### Запуск сервера

1. Запустіть розробницький сервер:

```shell
python manage.py runserver
```


2. Відкрийте у веб-браузері [http://localhost:8000](http://localhost:8000) для перегляду сайту.

## Адміністративний інтерфейс

1. Створіть суперкористувача:

```shell
python manage.py createsuperuser
```


2. Перейдіть до [http://localhost:8000/admin](http://localhost:8000/admin) та увійдіть, використовуючи облікові дані суперкористувача, щоб керувати товари та замовленнями через адміністративний інтерфейс.

## Внесення змін

Для внесення змін у моделі та відображення цих змін у базі даних:

1. Внесіть необхідні зміни в `models.py`.
2. Створіть нову міграцію:

```shell
python manage.py makemigrations
```

3. Застосуйте міграцію:

```shell
python manage.py migrate
```


## Тестування

Для запуску тестів використовуйте команду:


```shell
python manage.py test
```

Таким чином, цей `README.md` надає комплексне керівництво для нових розробників проекту або користувачів, які хочуть налаштувати та запустити ваш інтернет-магазин локально.
"""

# Writing the content to a README.md file




