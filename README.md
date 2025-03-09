# Medical Information System (MIS)

Медицинская информационная система (МИС) — это веб-сервис для управления консультациями пациентов с врачами. Проект включает функциональность для авторизации пользователей, управления консультациями, фильтрации, поиска и сортировки данных. Выполнен как тестовое задание.

## Основные функции

* **Авторизация пользователей** через JWT (access и refresh токены).
* **Управление консультациями** :
* Редактирование статуса консультаций.
* Фильтрация по статусу, поиск по ФИО врача и пациента, сортировка по дате.
* **Ролевая модель** :
* Администратор: полный доступ.
* Врач: доступ к своим консультациям.
* Пациент: доступ к своим консультациям.
* **Документация API** через Swagger.

## Технологии

* **Backend** : Django, Django REST Framework (DRF).
* **База данных** : PostgreSQL.
* **Аутентификация** : JWT (JSON Web Tokens).
* **Документация** : Swagger (OpenAPI 3.0).
* **Тестирование** : pytest.
* **Контейнеризация** : Docker, Docker Compose.

---

## Установка и запуск на локальной машине

### 1. Установите Docker и Docker Compose

Убедитесь, что у вас установлены Docker и Docker Compose. Если нет, следуйте официальной документации:

* [Установка Docker](https://docs.docker.com/get-docker/)
* [Установка Docker Compose](https://docs.docker.com/compose/install/)

### 2. Клонируйте репозиторий

bash

Copy

```
git clone https://github.com/Dmitded/mis_test.git
cd mis_test
```

### 3. Настройка переменных окружения

Создайте файл `.env` в папке deploy (пример в той же папке) и добавьте в него следующие переменные:

bash

Copy

```
# Настройки базы данных
POSTGRES_PASSWORD=mis_password
DB_HOST=db
DB_PORT=5432

# Настройки Django
SECRET_KEY=secret
DJANGO_SUPERUSER_USERNAME=mis_admin
DJANGO_SUPERUSER_PASSWORD=password
DJANGO_SUPERUSER_EMAIL=mis_admin@mail.ru
```

### 4. Запуск проекта

Соберите и запустите контейнеры:

bash

Copy

```
docker-compose up --build
```

После запуска проект будет доступен по адресу:
 **API** : `http://localhost:8000/api/v1`
 **Админ-панель** : `http://localhost:8000/admin`
 **Swagger документация** : `http://localhost:4321`

### 5. Создание суперпользователя

Чтобы получить доступ к админ-панели, создайте суперпользователя:

bash

Copy

```
docker-compose exec web python manage.py createsuperuser
```

Введите имя пользователя, email и пароль.

---

## Заполнение БД тестовыми данными

Внимание! Данный скрипт очищает всю БД, в т.ч. созданного суперпользователя!
Для запуска скрипта выполните следующую команду:

bash

Copy

```
docker-compose up test
```

Тесты проверяют функциональность API, включая авторизацию, управление консультациями, фильтрацию и сортировку.

---

## Запуск тестов

Для запуска тестов выполните следующую команду:

bash

Copy

```
docker-compose up test
```

Тесты проверяют функциональность API, включая авторизацию, управление консультациями, фильтрацию и сортировку.

---

## Использование API

### Авторизация

1. Получите токены:
   bash

   Copy

   ```
   POST /api/v1/auth
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
2. Используйте access токен для авторизации:
   bash

   Copy

   ```
   Authorization: Bearer <access_token>
   ```

### Примеры запросов

#### Получение списка консультаций

bash

Copy

```
GET /api/v1/consultations
```

#### Фильтрация по статусу

bash

Copy

```
GET /api/v1/consultations?status=confirmed
```

#### Поиск по ФИО врача

bash

Copy

```
GET /api/v1/consultations?doctor_name=Иван
```

#### Сортировка по дате (сначала новые)

bash

Copy

```
GET /api/v1/consultations?sort_asc=desc
```

#### Обновление статуса консультации

bash

Copy

```
PATCH /api/v1/consultations/{id}/status
{
  "status": "confirmed"
}
```

---

## Структура проекта

Copy

```
mis_test/
├── apps/
│   ├── domain/              # Доменные сущности и бизнес-логика
│   ├── application/         # Use cases
│   ├── infrastructure/      # Репозитории, модели, команды управления
│   └── presentation/        # API, views, сериализаторы
├── tests/                   # Тесты (интеграционные и unit)
├── docker-compose.yml       # Конфигурация Docker Compose
├── Dockerfile               # Dockerfile для основного приложения
├── requirements.txt         # Зависимости Python
├── deploy/                  # Файлы для деплоя проекта
│   └── .env                 # Переменные окружения
└── README.md                # Документация проекта
```

---

## Контакты

Если у вас есть вопросы или предложения, свяжитесь со мной:
 **Email** : [lutkovsky.dmitry@yandex.ru](https://mailto:lutkovsky.dmitry@yandex.ru/)
 **GitHub** : [Dmitded](https://github.com/Dmitded)
