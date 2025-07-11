## Модели данных

### Пользователь (`User`)

- `id:` Уникальный идентификатор пользователя (PK).
- `email:` Электронная почта. Используется как ``USERNAME_FIELD``.
- `phone:` Контактный номер телефона.
- `first_name:` Имя пользователя.
- `last_name:` Фамилия пользователя.
- `image:` Аватар пользователя.
- `role:` Роль пользователя в системе (см. :class:`~User.Roles`).
- `is_active:` Флаг активности пользователя. Неактивные не могут войти.
- `is_staff:` Флаг доступа к административной панели Django.
- `is_superuser:` Флаг, дающий все права без их явного назначения.
- `last_login:` Дата и время последнего входа.
- `date_joined:` Дата и время регистрации.

### Модель объекта сети поставок (`Node`):

Представляет собой элемент (объект сети) в иерархической структуре сети, будь то завод, розничная сеть или
индивидуальный
предприниматель.

- `id:` Уникальный идентификатор объекта сети (PK).
- `name:` Название объекта сети.
- `email:` Email-адрес.
- `phone:` Телефон.
- `country:` Страна.
- `city:` Город.
- `street:` Улица.
- `building_number:` Номер дома.
- `supplier:` Ссылка на поставщика (предыдущий по иерархии объект сети). Может быть ``None`` только для завода (уровень
  0).
- `debt_to_supplier:` Задолженность перед поставщиком.
- `created_at:` Дата и время создания записи (устанавливается автоматически).

### Модель продукта (`Product`):

Представляет продукт, который производится или продается звеном сети.

- `id:` Уникальный идентификатор продукта (PK).
- `name:` Название продукта.
- `model:` Модель продукта.
- `release_date:` Дата выхода продукта на рынок.
- `owner:` Звено сети, которому принадлежит продукт.

## API

🔁 Тип связей

- *Node — Node (supplier)*: Один-ко-многим (каждый объект сети может иметь много «клиентов», но одного
  «поставщика»)
- *Node — Product*: Один-ко-многим объект сети может продавать/владеть несколькими продуктами)

📐 Общая структура и иерархия
Сеть состоит из трех уровней:

1. *Завод* — всегда находится на нулевом уровне. У него нет поставщика, он — первоисточник продукции.
2. *Индивидуальный предприниматель (ИП)* — закупает продукцию у любого звена выше, включая завод или розничную сеть.
3. *Розничная сеть* — может закупать продукцию у завода или у другого звена, находящегося выше по иерархии.

Уровень звена определяется не названием, а глубиной цепочки поставок — числом переходов от узла до завода.

🛠️ Зачем такая структура и что это даёт на практике?

- Анализ глубины цепочек.
  Например: «сколько у нас 3-уровневых цепочек?»
  Или: «все ли розничные сети имеют хотя бы одного посредника?»
- Фильтрация и сортировка:
  Показать всех клиентов уровня 2 (от завода).
  Проверить, кто напрямую закупается у завода (level=1).
- Маржинальный анализ:
  Чем ниже узел, тем выше наценка и потенциальный риск задолженности.
- Модель может использовать уровень для расчёта логистики, скидок, сроков поставки и т.д.
- Визуализация структуры:
  Уровень помогает красиво отрисовать дерево, граф, диаграмму.

### Аутентификация и Пользователи

#### 1. Регистрация пользователя

- **POST** `/user/register/`
- **Request body:**
    ```json
    {
        "email": "user@example.com",
        "phone": "string",
        "first_name": "string",
        "last_name": "string",
        "password": "stringst",
        "password_confirmation": "string"
    }
    ```

#### 2. Получение JWT токенов (Вход)

- **POST** `/user/login/`
- **Request body:**
    ```json
    {
        "email": "user@example.com",
        "password": "password123"
    }
    ```
- **Response (200 OK):**
  ```json
  {
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

#### 3. Обновление Access токена

- **POST** `/user/token/refresh/`
- **Request body:**
  ```json
  {
      "refresh": "your_refresh_token"
  }
  ```
- **Response (200 OK):**
  ```json
  {
      "access": "new_access_token"
  }
  ```

### 4. Объект сети поставок

- **GET** `/supply/nodes/`: Получение списка всех объектов сети поставок.
    - Доступ: Авторизованные пользователи.
    - Поддерживает сортировку по стране (`country`) через query-параметр: `/supply/nodes/?country=<код страны>`,
      например `KZ`. (Реализовано с `django-filter`).
- **POST** `/supply/nodes/`: Создание нового объекта сети поставок.
    - Доступ: Авторизованные пользователи.
- **GET** `/supply/nodes/{id}/`: Получение конкретного объекта сети поставок.
    - Доступ: Авторизованные пользователи.
- **PUT/PATCH** `/supply/nodes/{id}/`: Обновление объекта сети поставок.
    - Доступ: Авторизованные пользователи.
- **DELETE** `/supply/nodes/{id}/`: Удаление ообъекта сети поставок.
    - Доступ: Авторизованные пользователи.
- **GET** `/supply/nodes/{node_id}/products/`: Получение списка продуктов, принадлежащих конкретному объекту сети.
    - Доступ: Авторизованные пользователи.
- **GET** `supply/nodes/{node_id}/products/{product_id}/`: Получение конкретного продукта, принадлежащего конкретному
  объекту сети.
    - Доступ: Авторизованные пользователи.
- **GET** `supply/products/`: Получение списка продуктов в сети поставок.
    - Доступ: Авторизованные пользователи.
- **POST** `/supply/products/`: Создание нового продукта в сети поставок.
    - Доступ: Авторизованные пользователи.
- **GET** `/supply/products/{id}/`: Получение конкретного продукта в сети поставок.
    - Доступ: Авторизованные пользователи.
- **PUT/PATCH** `/supply/products/{id}/`: Обновление продукта в сети поставок.
    - Доступ: Авторизованные пользователи.
- **DELETE** `/supply/products/{id}/`: Удаление продукта в сети поставок.
    - Доступ: Авторизованные пользователи.

## Права доступа (Permissions)

- **Анонимный пользователь:**
    - Не имеет доступа к API.

- **Авторизованный пользователь (`user`):**
    - Получать список объектов сети поставок (`GET /supply/nodes/`)
    - Создавать объект сети поставок (`POST /supply/nodes/`)
    - Получать один объект сети поставок (`GET /supply/nodes/{id}`)
    - Редактировать объект сети поставок (`PUT/PATCH /supply/nodes/{id}`)
    - Удалять объект сети поставок (`DELETE /supply/nodes/{id}`)
    - Получать список продуктов, принадлежащих конкретному объекту сети (`GET /supply/nodes/{node_id}/products/`)
    - Получать конкретный продукт, принадлежащий конкретному объекту сети (
      `GET /supply/nodes/{node_id}/products/{product_id}/`)
    - Получать список продуктов сети поставок (`GET /supply/products/`)
    - Создавать продукт сети поставок (`POST /supply/products/`)
    - Получать один продукт сети поставок (`GET /supply/products/{id}`)
    - Редактировать продукт сети поставок (`PUT/PATCH /supply/products/{id}`)
    - Удалять объект продукт поставок (`DELETE /supply/products/{id}`)
