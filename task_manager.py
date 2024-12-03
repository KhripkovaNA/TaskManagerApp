import json
from typing import List, Dict, Optional

from utils import present_task


class Task:
    _counter = 0

    def __init__(self, title: str, description: str, category: str, due_date: str,
                 priority: str, task_id: int = None, status: str = "не выполнена"):
        if task_id is None:
            Task._counter += 1
            self.id = Task._counter
        else:
            self.id = task_id
            Task._counter = max(Task._counter, task_id)
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def present_task(self) -> str:
        """Форматирует задачу для вывода"""
        return (f"ID: {self.id}, Название: {self.title}, Категория: {self.category}\n"
                f"\tОписание: {self.description}\n"
                f"\tСрок: {self.due_date}, Приоритет: {self.priority}, Статус: {self.status}"
                )

    def mark_as_completed(self):
        """Отметить задачу как выполненную"""
        self.status = "Выполнена"

    def edit(self, title: Optional[str] = None,
             description: Optional[str] = None,
             category: Optional[str] = None,
             due_date: Optional[str] = None,
             priority: Optional[str] = None):
        """Редактировать поля задачи"""
        if title:
            self.title = title
        if description:
            self.description = description
        if category:
            self.category = category
        if due_date:
            self.due_date = due_date
        if priority:
            self.priority = priority

    def to_dict(self) -> Dict:
        """Преобразует объект задачи в словарь для сохранения в JSON"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict) -> "Task":
        """Создает объект задачи из словаря"""
        return Task(
            task_id=data["id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data["status"]
        )

    def delete_task(self, task_id: int):
        """Удалить задачу по ID"""
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()

    def search_tasks(self, keyword: Optional[str] = None, category: Optional[str] = None, status: Optional[str] = None) -> List[Task]:
        """Поиск задач по ключевому слову, категории или статусу"""
        results = self.tasks
        if keyword:
            results = [task for task in results if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()]
        if category:
            results = [task for task in results if task.category.lower() == category.lower()]
        if status:
            results = [task for task in results if task.status.lower() == status.lower()]
        return results


class TaskManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.tasks: List[Task] = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        """Загружает задачи из JSON файла"""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                tasks = json.load(file)
                return [Task.from_dict(task) for task in tasks]
        except FileNotFoundError:
            return []

    def save_tasks(self) -> None:
        """Сохраняет задачи в JSON файл"""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, title: str, description: str, category: str, due_date: str, priority: str):
        """Добавляет новую задачу"""
        new_task = Task(title, description, category, due_date, priority)
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"Задача '{title}' добавлена с ID {new_task.id}")

    def list_tasks(self, category: Optional[str] = None) -> None:
        """Выводит список задач. Если указана категория, выводятся только задачи из этой категории"""
        if not self.tasks:
            print("Нет задач для отображения")
        else:
            # Фильтрация задач по категории
            filtered_tasks = self.tasks if not category else [task for task in self.tasks if
                                                              task.category.lower() == category.lower()]
            if not filtered_tasks:
                print(f"Нет задач в категории '{category}'")
            else:
                if category:
                    print(f"Список задач в категории '{category}':")
                else:
                    print("Список всех задач:")

                for task in filtered_tasks:
                    print(task.present_task())

    def get_task(self, task_id: int) -> None:
        """Получить задачу по ID"""
        task = next((task for task in self.tasks if task.id == task_id), None)
        if task:
            print(task.present_task())
    #
    # def update_status(self, book_id: int, new_status: str) -> None:
    #     """Обновляет статус книги по ID"""
    #     for book in self.books:
    #         if book.id == book_id:
    #             if book.status != new_status:
    #                 book.status = new_status
    #                 self.save_books()
    #                 print(f"Статус книги с ID {book_id} успешно обновлен на '{new_status}'")
    #             else:
    #                 print(f"Статус книги с ID {book_id} уже '{new_status}'")
    #             return
    #     print(f"Книга с ID {book_id} не найдена")
    #
    # def search_books(self, field: str, query: str) -> None:
    #     """Ищет книги по заданному полю"""
    #     results = [
    #         present_book(book)
    #         for book in self.books
    #         if query.lower() in str(getattr(book, field, "")).lower()
    #     ]
    #     if results:
    #         print(conjugate_books(len(results)))
    #         print(*results, sep='\n')
    #     else:
    #         print("Книги по заданному запросу не найдены")
    #
    # def delete_book(self, book_id: int) -> None:
    #     """Удаляет книгу по ID"""
    #     for book in self.books:
    #         if book.id == book_id:
    #             self.books.remove(book)
    #             self.save_books()
    #             print(f"Книга с ID {book_id} успешно удалена")
    #             return
    #     print(f"Книга с ID {book_id} не найдена")
