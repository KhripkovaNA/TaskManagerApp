from typing import Dict


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
        padding = " " * len(f"ID: {self.id}, ")
        return (f"ID: {self.id}, Название: {self.title}, Категория: {self.category}\n"
                f"{padding}Описание: {self.description}\n"
                f"{padding}Срок: {self.due_date}, Приоритет: {self.priority}, Статус: {self.status}")

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
