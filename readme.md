## Telegram-бот для студентов

### Разработка

```bash
 python -m src.app
```

### Функции

- Привязка GitHub-аккаунта
- Получение оповещений
- Просмотр статистики по решенным заданиям
- Возможность оспорить оценку


### Запуск контейнеров для разработки
Контейнер приложения запускается в reload-режиме для разработки
```bash
docker compose -f dev.docker-compose.yaml build
docker compose -f dev.docker-compose.yaml up -d
```