# Система Аутентификации и Авторизации

Проект реализует собственную систему аутентификации и авторизации с гибкой системой управления правами доступа.

## 🚀 Основные возможности

- **Регистрация и аутентификация** пользователей
- **JWT токены** для безопасного доступа
- **Гибкая система ролей и прав** доступа
- **CRUD операции** с проверкой прав
- **Мягкое удаление** пользователей
- **Полное покрытие тестами**

## 🛠 Технологии

- **FastAPI** - современный Python фреймворк
- **PostgreSQL** - реляционная база данных
- **SQLAlchemy** - ORM для работы с БД
- **JWT** - JSON Web Tokens для аутентификации
- **bcrypt** - хеширование паролей
- **Pytest** - тестирование

## 📁 Структура проекта
```
auth_system/
├── database/
│ └── db.py # Настройка базы данных
├── models/
│ ├── user.py # Модель пользователя
│ ├── role.py # Модель ролей
│ ├── product.py # Модель продукта
│ └── access_roles_rules.py # Правила доступа
├── routes/
│ ├── auth.py # Эндпоинты аутентификации
│ ├── user_router.py # Эндпоинты пользователей
│ └── resource_router.py # Эндпоинты ресурсов
├── middlewares/
│ ├── auth_middleware.py # Middleware аутентификации
│ └── authorization.py # Проверка прав доступа
├── utils/
│ └── security.py # Утилиты безопасности
├── tests/
│ └── test_simple.py # Тесты
├── services/
│ ├── init_roles.py # Инициализация ролей
│ └── user_service.py # Сервис пользователей
├── main.py # Основное приложение
├── init_db.py # Инициализация БД
└── requirements.txt # Зависимости
```

## 🗄️ Архитектура базы данных

### Модель прав доступа
```
Users (Пользователи)
├── id
├── first_name
├── last_name
├── email
├── hashed_password
├── role_id (FK → Roles.id)
└── is_active

Roles (Роли)
├── id
├── name (admin, user)
└── description

AccessRolesRules (Правила доступа)
├── id
├── role_id (FK → Roles.id)
├── element (users, products)
├── read_permission
├── read_all_permission
├── create_permission
├── update_permission
├── update_all_permission
├── delete_permission
└── delete_all_permission

Products (Продукты)
├── id
├── name
├── description
└── owner_id (FK → Users.id)
```

### Система прав

- **admin** - полный доступ ко всем операциям
- **user** - ограниченные права на свои данные
- **Гибкая настройка** через таблицу `AccessRolesRules`

## ⚡ Быстрый старт

### 1. Клонирование и настройка

```bash
git clone <repository-url>
cd auth_system
python -m venv auth_system_env

# Для Windows:
auth_system_env\Scripts\activate
# Для Linux/Mac:
source auth_system_env/bin/activate

pip install -r requirements.txt
```

### 2. Настройка базы данных

Создайте базу данных PostgreSQL и обновите DATABASE_URL в database/db.py:

```
DATABASE_URL = "postgresql://username:password@localhost/db_name"
```
### 3. Инициализация БД
```
python init_db.py
```

Создается:

- **Роли:** admin и user

- **Администратор:** admin@example.com / admin123

- Правила доступа по умолчанию

### 4. Запуск приложения
```
python main.py
```

#### Приложение доступно по адресу: http://127.0.0.1:8000

#### Документация API: http://127.0.0.1:8000/docs

## 🔑 API Endpoints


### Аутентификация
```
Метод	Endpoint	Описание
POST	/auth/register	Регистрация пользователя
POST	/auth/login	Вход в систему
```

### Пользователи
```
Метод	Endpoint	Права доступа
GET	/users/me	Текущий пользователь
PATCH	/users/me	Обновление профиля
DELETE	/users/me	Удаление аккаунта
GET	/users/all	Только admin
POST	/users/logout	Все пользователи
```

### Ресурсы (Продукты)
```
Метод	Endpoint	Права доступа
GET	/resource/products	Чтение своих/всех
POST	/resource/products	Создание
PUT	/resource/products/{id}	Обновление своих/всех
DELETE	/resource/products/{id}	Удаление своих/всех
```

## 📝 Примеры использования

### 1. Регистрация пользователя
```
curl -X POST "http://127.0.0.1:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Иван",
       "last_name": "Петров",
       "email": "ivan@example.com",
       "password": "securepassword123"
     }'
```

### 2. Вход в систему
```
curl -X POST "http://127.0.0.1:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "ivan@example.com",
       "password": "securepassword123"
     }'
```
#### Ответ:
```
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### 3. Доступ к защищенному эндпоинту
```
curl -X GET "http://127.0.0.1:8000/users/me" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
### 4. Создание продукта
```
curl -X POST "http://127.0.0.1:8000/resource/products" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Мой продукт",
       "description": "Описание продукта"
     }'
```

## 🧪 Тестирование
#### Запуск тестов:
```
pytest tests/test_simple.py -v
```

#### Тесты покрывают:

✅ Основные эндпоинты

✅ Полный цикл аутентификации

✅ Проверку прав доступа

✅ CRUD операции

✅ Ошибки доступа

#### 🔒 Безопасность
- Пароли хешируются с помощью bcrypt

- Аутентификация через JWT токены

- Проверка прав доступа для каждого запроса

- Защита от несанкционированного доступа

- Валидация входных данных

### 👨‍💻 Разработка
#### Добавление новых ресурсов
- Создайте модель в models/

- Добавьте правила доступа в init_db.py

- Создайте роутер по примеру resource_router.py

- Добавьте роутер в main.py
