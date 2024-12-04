import pytest
from app.task_manager import TaskManager


@pytest.fixture
def task_manager(tmp_path):
    """Создает временный экземпляр TaskManager с тестовым файлом"""
    test_file = f"{tmp_path}/test_tasks.json"
    return TaskManager(test_file)


def test_add_task(task_manager, capsys):
    """Тест добавления задачи"""
    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )

    output = capsys.readouterr().out
    assert len(task_manager.tasks) == 1
    task = task_manager.tasks[0]
    assert task.description == "Пройти основы языка"
    assert task.category == "Обучение"
    assert task.due_date == "30.01.2025"
    assert task.priority == "высокий"
    assert f"Задача 'Изучить Python' добавлена с ID {task.id}" in output


def test_list_tasks(task_manager, capsys):
    """Тест вывода списка задач"""
    task_manager.list_tasks()
    output = capsys.readouterr().out
    assert "Нет задач для отображения" in output

    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )
    task_manager.add_task(
        title="Пройти курс Django",
        description="Изучить основы Django",
        category="Работа",
        due_date="20.12.2024",
        priority="средний"
    )

    task_manager.list_tasks()
    output = capsys.readouterr().out
    assert "Изучить Python" in output
    assert "Изучить основы Django" in output

    task_manager.list_tasks(category="Обучение")
    output = capsys.readouterr().out
    assert "Список задач в категории 'Обучение':" in output
    assert "Изучить Python" in output
    assert "Изучить основы Django" not in output

    task_manager.list_tasks(category="Личное")
    output = capsys.readouterr().out
    assert "Нет задач в категории 'Личное'" in output


def test_get_task(task_manager):
    """Тест получения задачи по ID"""
    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )
    task_id = task_manager.tasks[0].id
    task = task_manager.get_task(task_id=task_id)
    assert task is not None
    assert task.title == "Изучить Python"

    task = task_manager.get_task(task_id=task_id + 1)
    assert task is None


def test_get_tasks(task_manager):
    """Тест получения задач по ключевому слову, категории или статусу"""
    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )
    task_manager.add_task(
        title="Пройти курс Django",
        description="Изучить основы Django",
        category="Работа",
        due_date="20.12.2024",
        priority="средний"
    )
    task_manager.add_task(
        title="Изучить Flask",
        description="Основы Flask",
        category="Обучение",
        due_date="01.01.2025",
        priority="низкий"
    )

    tasks = task_manager.get_tasks(keyword="Python")
    assert len(tasks) == 1
    assert tasks[0].title == "Изучить Python"

    tasks = task_manager.get_tasks(keyword="основы")
    assert len(tasks) == 3

    tasks = task_manager.get_tasks(category="Обучение")
    assert len(tasks) == 2
    assert tasks[1].title == "Изучить Flask"

    tasks = task_manager.get_tasks(status="выполнена")
    assert len(tasks) == 0


def test_edit_task(task_manager, capsys):
    """Тест редактирования задачи"""
    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )

    task_id = task_manager.tasks[0].id
    task_manager.edit_task(task_id, title="Изучить Django", priority="средний")
    output = capsys.readouterr().out
    task = task_manager.tasks[0]
    assert task.title == "Изучить Django"
    assert task.priority == "средний"
    assert f"Задача с ID {task_id} успешно отредактирована" in output

    invalid_task_id = task_id + 1
    task_manager.edit_task(invalid_task_id, title="Изучить Django", priority="средний")
    output = capsys.readouterr().out
    assert f"Задача с ID {invalid_task_id} не найдена" in output


def test_update_status(task_manager, capsys):
    """Тест обновления статуса задачи"""
    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )

    task_id = task_manager.tasks[0].id
    task_manager.update_status(task_id)
    output = capsys.readouterr().out
    task = task_manager.tasks[0]
    assert task.status == "выполнена"
    assert f"Задача с ID {task_id} отмечена как 'выполнена'" in output

    task_manager.update_status(task_id)
    output = capsys.readouterr().out
    assert f"Задача с ID {task_id} уже отмечена как 'выполнена'" in output

    invalid_task_id = task_id + 1
    task_manager.update_status(invalid_task_id)
    output = capsys.readouterr().out
    assert f"Задача с ID {invalid_task_id} не найдена" in output


def test_delete_task_by_id(task_manager, capsys):
    """Тест удаления задачи по ID"""
    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )

    task_id = task_manager.tasks[0].id
    task_manager.delete_tasks(task_id=task_id)
    output = capsys.readouterr().out
    assert len(task_manager.tasks) == 0
    assert f"Задача с ID {task_id} успешно удалена" in output

    task_manager.delete_tasks(task_id=task_id)
    output = capsys.readouterr().out
    assert f"Задача с ID {task_id} не найдена" in output


def test_delete_tasks_by_category(task_manager, capsys):
    """Тест удаления задач по категории"""
    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )
    task_manager.add_task(
        title="Пройти курс Django",
        description="Изучить основы Django",
        category="Работа",
        due_date="20.12.2024",
        priority="средний"
    )
    task_manager.add_task(
        title="Изучить Flask",
        description="Основы Flask",
        category="Обучение",
        due_date="01.01.2025",
        priority="низкий"
    )

    task_manager.delete_tasks(category="Обучение")
    output = capsys.readouterr().out
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].category == "Работа"
    assert "Задачи из категории 'Обучение' успешно удалены" in output

    task_manager.delete_tasks(category="Обучение")
    output = capsys.readouterr().out
    assert len(task_manager.tasks) == 1
    assert "Задачи из категории 'Обучение' не найдены" in output


def test_search_tasks(task_manager, capsys):
    """Тест поиска задач"""
    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )
    task_manager.add_task(
        title="Пройти курс Django",
        description="Изучить основы Django",
        category="Работа",
        due_date="20.12.2024",
        priority="средний"
    )
    task_manager.add_task(
        title="Изучить Flask",
        description="Основы Flask",
        category="Обучение",
        due_date="01.01.2025",
        priority="низкий"
    )

    task_manager.search_tasks(keyword="Python")
    output = capsys.readouterr().out
    assert "Изучить Python" in output

    task_manager.search_tasks(category="Работа")
    output = capsys.readouterr().out
    assert "Пройти курс Django" in output
    assert "Изучить Python" not in output

    task_manager.search_tasks(status="выполнена")
    output = capsys.readouterr().out
    assert "Задачи по заданному запросу не найдены" in output
