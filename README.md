# Landscape

**Основа асинхронного сервиса с фоновыми задачами, реактивным состоянием и потоковой передачей файлов.**

Объединяет работу с внешними API, выполнение задач и наблюдение за прогрессом через HTTP и WebSocket. Прикладная логика располагается в app.core, общие механизмы — в app.tools.

**Python · FastAPI · aiohttp · Pydantic · PostgreSQL · Docker Compose**

## Особенности

**[Задачи с подпиской](https://github.com/sdvezhenkov/landscape/blob/master/app/tools/essential/task/task_base.py).** Запуск через HTTP, независимые снимки состояния для клиентов WebSocket. Завершённая задача возвращает итог и закрывает соединение.

**[Реактивные модели](https://github.com/sdvezhenkov/landscape/blob/master/app/tools/essential/task/types/task_state.py).** Изменение поля автоматически запускает публикацию состояния. [Реестр](https://github.com/sdvezhenkov/landscape/blob/master/app/tools/essential/task/task_registry.py) ограничивает активные задачи и очищает завершённые.

**[Потоковая передача](https://github.com/sdvezhenkov/landscape/blob/master/app/tools/essential/request/pipe/pipe/pipe.py).** Скачивание и загрузка работают параллельно через ограниченную очередь, без сборки файла целиком в памяти. При сбое предусмотрен [повтор передачи](https://github.com/sdvezhenkov/landscape/blob/master/app/tools/essential/request/pipe/retry_pipe/retry_pipe.py).

**[Конкурентный кэш](https://github.com/sdvezhenkov/landscape/blob/master/app/tools/essential/cache/cache.py).** Одинаковые асинхронные вызовы ожидают общий результат без дублирования запросов.

**[HTTP-повторы](https://github.com/sdvezhenkov/landscape/blob/master/app/tools/essential/request/session/retry/retry_middleware/get_retry_middleware.py).** Политика методов, статусов и таймаутов; экспоненциальная задержка с jitter.

**[OIDC / JWT](https://github.com/sdvezhenkov/landscape/blob/master/app/tools/essential/security/auth/dependencies.py).** Проверка scopes и срока действия токена, включая открытые WebSocket-соединения. Swagger поддерживает Authorization Code с PKCE.

## Пример приложения

[API](https://github.com/sdvezhenkov/landscape/blob/master/app/core/api/user_api.py) получает пользователей и публикации из [JSONPlaceholder](https://jsonplaceholder.typicode.com/). [Client](https://github.com/sdvezhenkov/landscape/blob/master/app/core/client/user_client.py) обрабатывает данные, [task](https://github.com/sdvezhenkov/landscape/blob/master/app/core/task/get_user_names_task.py) выполняет операцию и обновляет прогресс. Прикладные модели и функции находятся в [app.core.tools](https://github.com/sdvezhenkov/landscape/blob/master/app/core/tools/task/types/example_state.py).

## Тестирование

**[Сквозные сценарии](https://github.com/sdvezhenkov/landscape/blob/master/app/tests/test_examples.py)** — HTTP-запуск, обработка ответа внешнего API, прогресс, результат и повторное подключение WebSocket. Внешний сервис воспроизводится локально.

**[Сбои передачи](https://github.com/sdvezhenkov/landscape/blob/master/app/tools/essential/request/pipe/pipe/tests/test_pipe.py)** и **[жизненный цикл задач](https://github.com/sdvezhenkov/landscape/blob/master/app/tools/essential/task/tests/test_task_base_run_bg.py)** — ошибки, подписки и [сериализация состояния](https://github.com/sdvezhenkov/landscape/blob/master/app/tools/essential/task/tests/test_task_base_serialization.py).

## Окружение

Интеграция с **[Aether](https://github.com/sdvezhenkov/aether)**: Docker Compose для [разработки](https://github.com/sdvezhenkov/landscape/blob/master/services/docker/docker-compose.dev.yml) и [развёртывания](https://github.com/sdvezhenkov/landscape/blob/master/services/docker/docker-compose.prod.yml). Задачи и их прогресс хранятся в памяти процесса.
