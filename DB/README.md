# Структура папки DB

В этой папке содержатся скрипты инициализации для различных баз данных, используемых в проекте.

## Структура директорий

- `init-script/`: Содержит SQL-скрипты для создания таблиц в базах данных.
  - `source_1/`: Скрипты для базы данных `source_1`.
  - `source_2/`: Скрипты для базы данных `source_2`.
  - `consumer_1/`: Скрипты для базы данных `consumer_1`.

## Описание баз данных и таблиц

### База данных: `source_1`

Эта база данных содержит информацию о пользователях.

**Таблица: `users`**

| Колонка    | Тип             | Описание                               |
|------------|-----------------|----------------------------------------|
| `id`       | `serial`        | PRIMARY KEY, Уникальный идентификатор  |
| `name`     | `varchar(255)`  | Имя пользователя                       |
| `email`    | `varchar(255)`  | Электронная почта пользователя         |
| `country_id`| `integer`       | ID страны (внешний ключ)               |
| `create_dt`| `TIMESTAMP`     | Дата и время создания записи           |

---

### База данных: `source_2`

Эта база данных содержит справочник стран.

**Таблица: `country`**

| Колонка    | Тип             | Описание                               |
|------------|-----------------|----------------------------------------|
| `id`       | `serial`        | PRIMARY KEY, Уникальный идентификатор  |
| `name`     | `varchar(255)`  | Название страны                        |
| `create_dt`| `TIMESTAMP`     | Дата и время создания записи           |

---

### База данных: `consumer_1`

Эта база данных является потребителем данных из `source_1` и `source_2` и содержит объединенную информацию.

**Таблица: `users`**

| Колонка    | Тип             | Описание                               |
|------------|-----------------|----------------------------------------|
| `id`       | `serial`        | PRIMARY KEY, Уникальный идентификатор  |
| `name`     | `varchar(255)`  | Имя пользователя                       |
| `email`    | `varchar(255)`  | Электронная почта пользователя         |
| `country_id`| `integer`       | ID страны (внешний ключ)               |
| `create_dt`| `TIMESTAMP`     | Дата и время создания записи           |

**Таблица: `country`**

| Колонка    | Тип             | Описание                               |
|------------|-----------------|----------------------------------------|
| `id`       | `serial`        | PRIMARY KEY, Уникальный идентификатор  |
| `name`     | `varchar(255)`  | Название страны                        |
| `create_dt`| `TIMESTAMP`     | Дата и время создания записи           |
