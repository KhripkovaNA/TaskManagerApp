import pytest
from app.task_manager import TaskManager


@pytest.fixture
def task_manager(tmp_path):
    """Создаёт временный экземпляр TaskManager с тестовым файлом."""
    test_file = tmp_path / "test_tasks.json"
    return TaskManager(test_file)


def test_add_task(task_manager):
    """Тест добавления задачи"""
    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.11.2024",
        priority="высокий"
    )
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == "Изучить Python"


def test_edit_task(task_manager):
    """Тест редактирования задачи"""
    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.11.2024",
        priority="высокий"
    )
    task_id = task_manager.tasks[0].id
    task_manager.edit_task(task_id, title="Изучить Django")
    assert task_manager.tasks[0].title == "Изучить Django"


def test_delete_task_by_id(task_manager):
    """Тест удаления задачи по ID"""
    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.11.2024",
        priority="высокий"
    )
    task_id = task_manager.tasks[0].id
    task_manager.delete_tasks(task_id)
    assert len(task_manager.tasks) == 0


def test_delete_tasks_by_category(task_manager):
    """Тест удаления задач по категории."""
    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.11.2024",
        priority="высокий"
    )
    task_manager.add_task(
        title="Пройти курс Django",
        description="Изучить основы Django",
        category="Работа",
        due_date="01.12.2024",
        priority="средний"
    )
    task_manager.delete_tasks(category="Обучение")
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].category == "Работа"


def test_search_tasks(task_manager, capfd):
    """Тест поиска задач"""
    task_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.11.2024",
        priority="высокий"
    )
    task_manager.add_task(
        title="Пройти курс Django",
        description="Изучить основы Django",
        category="Работа",
        due_date="01.12.2024",
        priority="средний"
    )
    task_manager.search_tasks(keyword="Python")
    out, err = capfd.readouterr()
    assert "Изучить Python" in out
