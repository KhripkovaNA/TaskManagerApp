## TaskManagerApp

**TaskManagerApp** — это консольное приложение для управления списком задач. Программа предоставляет возможности добавления, редактирования, удаления, поиска задач и просмотра списка задач по категориям. Хранение данных осуществляется в формате JSON, а функционал реализован с использованием Python.

---

### Функциональность

1. **Просмотр задач:**
   - Просмотр всех текущих задач
   - Фильтрация задач по категориям

2. **Добавление задач:**
   - Указание названия, описания, категории, срока выполнения и приоритета (низкий/средний/высокий)

3. **Редактирование задач:**
   - Изменение полей существующих задач
   - Возможность пометить задачу как выполненную

4. **Удаление задач:**
   - Удаление задач по ID
   - Удаление всех задач из указанной категории

5. **Поиск задач:**
   - Поиск по ключевым словам, категориям или статусу выполнения

---

## **Технологии**

- **Python 3.10+**
- Работа с консолью через стандартный модуль `builtins.input`
- **JSON** для хранения данных.
- **pytest** для тестирования

---

### Структура проекта

```
    TaskManagerApp/
    ├── main.py                     # Основной файл приложения
    ├── app/
    │   ├── __init__.py             
    │   ├── service.py              # Логика взаимодействия пользователя с репозиторием
    │   ├── task.py                 # Реализация класса Task
    │   └── task_manager.py         # Реализация класса TaskManager
    ├── tasks.json                  # JSON-файл для хранения данных о задачах
    ├── tests/                      # Тесты для проверки функциональности
    │   ├── __init__.py             
    │   ├── test_service.py         # Тесты для service.py
    │   └── test_task_manager.py    # Тесты для task_manager.py
    ├── README.md                   # Документация проекта
    ├── requirements.txt            # Список зависимостей
    └── .gitignore                  # Исключения для Git
```

---

### Установка и запуск

- Убедитесь, что у вас установлен Python 3.10 или выше

- **Клонирование репозитория**

Клонируйте проект с помощью Git:

```bash
git clone https://github.com/KhripkovaNA/TaskManagerApp.git
cd TaskManagerApp
```

- **Установка зависимостей**

Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate     # Для Windows
pip install -r requirements.txt
```

- **Запуск приложения**

Запустите приложение с помощью команды:

```bash
python main.py
```

Следуйте инструкциям в консоли для работы с задачами

---

### Тестирование

Для запуска всех тестов используйте команду:

```bash
pytest tests/
```
