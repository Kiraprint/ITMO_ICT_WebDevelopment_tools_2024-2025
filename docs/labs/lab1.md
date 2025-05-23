# Лабораторная работа 1: Реализация серверного приложения FastAPI

## Цель

Целью данной лабораторной работы является создание серверного приложения с использованием фреймворка FastAPI для управления пользователями, командами, проектами, навыками и задачами для платформы командного сотрудничества.

## Реализация

### Архитектура

- Использовали FastAPI для создания REST API
- SQLModel (надстройка над SQLAlchemy) для работы с базой данных PostgreSQL
- JWT-токены для аутентификации
- Docker для контейнеризации

### Основные модели данных

- User (пользователи)
- Team (команды)
- Project (проекты)
- Skill (навыки)
- Task (задачи)
- Связующие таблицы (UserSkillLink, TeamMemberLink, ProjectTeamLink и др.)

### Ключевые эндпоинты

- Аутентификация (/auth/register, /auth/login, /auth/me)
- Управление пользователями (/users/*)
- Управление командами (/teams/*)
- Управление проектами (/projects/*)
- Управление навыками (/skills/*)
- Управление задачами (/tasks/*)

### Документация

- Создали подробную документацию API с примерами запросов и ответов
- Документировали структуру базы данных
- Добавили инструкции по развертыванию с Docker
- Настроили MkDocs для удобного просмотра документации

### Безопасность

- Реализовали JWT-аутентификацию
- Хеширование паролей с bcrypt
- Проверка прав доступа для защищенных эндпоинтов

### Дополнительные функции

- Поиск пользователей по навыкам
- Фильтрация задач по статусу
- Связывание пользователей с командами и проектами

API предоставляет полный набор CRUD-операций для всех основных сущностей и обеспечивает гибкий поиск и фильтрацию данных для эффективного формирования команд разработчиков.
