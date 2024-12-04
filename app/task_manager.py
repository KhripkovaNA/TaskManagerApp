import json
from typing import List, Optional
from app.task import Task


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

    def get_task(self, task_id: int) -> Task:
        """Получает задачу по ID"""
        return next((task for task in self.tasks if task.id == task_id), None)

    def get_tasks(self, keyword: Optional[str] = None, category: Optional[str] = None,
                  status: Optional[str] = None) -> List[Task]:
        """Получает задачи по ключевому слову, категории или статусу"""
        if keyword:
            return [task for task in self.tasks if
                    keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()]
        if category:
            return [task for task in self.tasks if task.category.lower() == category.lower()]
        if status:
            return [task for task in self.tasks if task.status.lower() == status.lower()]

    def edit_task(self, task_id: int,
                  title: Optional[str] = None,
                  description: Optional[str] = None,
                  category: Optional[str] = None,
                  due_date: Optional[str] = None,
                  priority: Optional[str] = None) -> None:
        """Редактирует задачу по ID"""
        task = self.get_task(task_id)
        if not task:
            print(f"Задача с ID {task_id} не найдена")
        else:
            if title:
                task.title = title
            if description:
                task.description = description
            if category:
                task.category = category
            if due_date:
                task.due_date = due_date
            if priority:
                task.priority = priority
            self.save_tasks()
            print(f"Задача с ID {task_id} успешно отредактирована")

    def update_status(self, task_id: int) -> None:
        """Обновляет статус задачи по ID на 'выполнена'"""
        task = self.get_task(task_id)
        if not task:
            print(f"Задача с ID {task_id} не найдена")
        else:
            if task.status != "выполнена":
                task.status = "выполнена"
                self.save_tasks()
                print(f"Задача с ID {task_id} отмечена как 'выполнена'")
            else:
                print(f"Задача с ID {task_id} уже отмечена как 'выполнена'")

    def delete_tasks(self, task_id: Optional[int] = None, category: Optional[str] = None) -> None:
        """Удаляет задачи по ID или категории"""
        if task_id:  # Удаление задачи по ID
            task = self.get_task(task_id)
            if not task:
                print(f"Задача с ID {task_id} не найдена")
            else:
                self.tasks.remove(task)
                self.save_tasks()
                print(f"Задача с ID {task_id} успешно удалена")

        if category:  # Удаление задач по категории
            tasks = self.get_tasks(category=category)
            if tasks:
                self.tasks = [task for task in self.tasks if task not in tasks]
                self.save_tasks()
                print(f"Задачи из категории '{category}' успешно удалены")
            else:
                print(f"Задачи из категории '{category}' не найдены")

    def search_tasks(self, keyword: Optional[str] = None, category: Optional[str] = None,
                     status: Optional[str] = None) -> None:
        """Поиск задач по ключевому слову, категории или статусу"""
        results = []
        if keyword:
            results = self.get_tasks(keyword=keyword)
        if category:
            results = self.get_tasks(category=category)
        if status:
            results = self.get_tasks(status=status)
        if results:
            print("Результаты поиска:")
            print(*[task.present_task() for task in results], sep='\n')
        else:
            print("Задачи по заданному запросу не найдены")
