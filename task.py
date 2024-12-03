def present_task(task: "Task") -> str:
    return (
        f"""
        ID: {task.id}, Название: {task.title}, Категория: {task.category}
        \tОписание: {task.description}
        \tСрок выполнения: {task.due_date}, Статус: {task.status}
        """
    )
