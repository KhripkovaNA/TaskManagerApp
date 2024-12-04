import pytest
from app.task_manager import TaskManager
from app.service import (
    list_tasks, add_task, edit_task, update_status, delete_task, search_tasks, edit_task_by_field
)


@pytest.fixture
def tasks_manager(tmp_path):
    """Создает временный экземпляр TaskManager с тестовым файлом"""
    test_file = f"{tmp_path}/test_tasks.json"
    return TaskManager(test_file)


def test_list_tasks(tasks_manager, monkeypatch, capsys):
    """Тест функции просмотра задач"""
    list_tasks(tasks_manager, option="1")
    output = capsys.readouterr().out
    assert "Нет задач для отображения" in output

    tasks_manager.add_task(
        title="Изучить Python",
        description="пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )

    list_tasks(tasks_manager, option="1")
    output = capsys.readouterr().out
    assert "Изучить Python" in output

    monkeypatch.setattr("builtins.input", lambda _: "обучение")
    list_tasks(tasks_manager, option="2")
    output = capsys.readouterr().out
    assert "Изучить Python" in output

    monkeypatch.setattr("builtins.input", lambda _: "отмена")
    list_tasks(tasks_manager, option="2")
    output = capsys.readouterr().out
    assert "Просмотр задач отменен" in output

    inputs = iter(["   ", " отмена  "])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    list_tasks(tasks_manager, option="2")
    output = capsys.readouterr().out
    assert "Введена пустая строка!" in output


def test_add_task(tasks_manager, monkeypatch, capsys):
    """Тест функции добавления задачи"""
    inputs = iter([
        "изучить Python", "пройти основы языка", "обучение", "30.01.2025", "Высокий"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    add_task(tasks_manager)
    output = capsys.readouterr().out
    assert len(tasks_manager.tasks) == 1
    task = tasks_manager.tasks[0]
    assert task.title == "Изучить Python"
    assert task.description == "Пройти основы языка"
    assert task.category == "Обучение"
    assert task.priority == "высокий"
    assert "Добавление задачи отменено" not in output

    inputs = iter(["Пройти курс Django", "Изучить основы Django", "отмена"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    add_task(tasks_manager)
    output = capsys.readouterr().out
    assert len(tasks_manager.tasks) == 1
    assert "Добавление задачи отменено" in output

    inputs = iter(["Пройти курс Django", "   ", "Изучить основы Django",
                   "обучение", "2024-12-20", "20.12.2024", "ср", "средний"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    add_task(tasks_manager)
    output = capsys.readouterr().out
    assert len(tasks_manager.tasks) == 2
    assert "Введена пустая строка!" in output
    assert "Некорректный формат даты! Используйте формат дд.мм.гггг" in output
    assert "Некорректный приоритет задачи! Используйте: низкий, средний или высокий" in output
    assert "Добавление задачи отменено" not in output


def test_edit_task_by_field(monkeypatch, capsys):
    """Тест функции редактирования задачи по полям"""
    inputs = iter(["1", "изучить Django", "2", "изучить основы Django",
                   "3", "работа", "4", "20.12.2024", "5", "средний"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    expected_result = {
        "title": "Изучить Django",
        "description": "Изучить основы Django",
        "category": "Работа",
        "due_date": "20.12.2024",
        "priority": "средний",
    }
    result_dict = edit_task_by_field()
    assert result_dict == expected_result


def test_edit_task(tasks_manager, monkeypatch, capsys):
    """Тест функции редактирования задачи"""
    tasks_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )
    task_id = tasks_manager.tasks[0].id

    inputs = iter([str(task_id), "1", "Изучить Django", "завершить"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    edit_task(tasks_manager)
    output = capsys.readouterr().out
    assert tasks_manager.tasks[0].title == "Изучить Django"
    assert "Редактирование задачи завершено" in output

    inputs = iter([str(task_id), "1", "Изучить Python", "отмена"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    edit_task(tasks_manager)
    output = capsys.readouterr().out
    assert tasks_manager.tasks[0].title == "Изучить Django"
    assert "Редактирование задачи отменено" in output

    invalid_task_id = task_id + 1
    inputs = iter(["один", "-1", str(invalid_task_id)])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    edit_task(tasks_manager)
    output = capsys.readouterr().out
    assert "Некорректный ID! Введите число" in output
    assert "Некорректный ID! ID должно быть положительным числом" in output
    assert f"Задача с ID {invalid_task_id} не найдена" in output


def test_update_status(tasks_manager, monkeypatch, capsys):
    """Тест функции обновления статуса задачи"""
    tasks_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )
    task_id = tasks_manager.tasks[0].id

    monkeypatch.setattr("builtins.input", lambda _: str(task_id))
    update_status(tasks_manager)
    output = capsys.readouterr().out
    assert tasks_manager.tasks[0].status == "выполнена"
    assert f"Задача с ID {task_id} отмечена как 'выполнена'" in output

    monkeypatch.setattr("builtins.input", lambda _: str(task_id))
    update_status(tasks_manager)
    output = capsys.readouterr().out
    assert tasks_manager.tasks[0].status == "выполнена"
    assert f"Задача с ID {task_id} уже отмечена как 'выполнена'" in output

    invalid_task_id = task_id + 1
    inputs = iter(["один", "-1", str(invalid_task_id)])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    update_status(tasks_manager)
    output = capsys.readouterr().out
    assert "Некорректный ID! Введите число" in output
    assert "Некорректный ID! ID должно быть положительным числом" in output
    assert f"Задача с ID {invalid_task_id} не найдена" in output


def test_delete_task_by_id(tasks_manager, monkeypatch, capsys):
    """Тест функции удаления задачи по ID"""
    tasks_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )
    task_id = tasks_manager.tasks[0].id

    inputs = iter([str(task_id), "да"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    delete_task(tasks_manager, option="id")
    output = capsys.readouterr().out
    assert len(tasks_manager.tasks) == 0
    assert f"Задача с ID {task_id} успешно удалена" in output

    inputs = iter(["один", "-1", str(task_id)])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    delete_task(tasks_manager, option="id")
    output = capsys.readouterr().out
    assert "Некорректный ID! Введите число" in output
    assert "Некорректный ID! ID должно быть положительным числом" in output
    assert f"Задача с ID {task_id} не найдена" in output


def test_delete_task_by_category(tasks_manager, monkeypatch, capsys):
    """Тест функции удаления задачи по категории"""
    tasks_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )
    tasks_manager.add_task(
        title="Пройти курс Django",
        description="Изучить основы Django",
        category="Работа",
        due_date="20.12.2024",
        priority="средний"
    )
    tasks_manager.add_task(
        title="Изучить Flask",
        description="Основы Flask",
        category="Обучение",
        due_date="01.01.2025",
        priority="низкий"
    )

    capsys.readouterr()
    inputs = iter(["Работа", "да"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    delete_task(tasks_manager, option="category")
    output = capsys.readouterr().out
    assert len(tasks_manager.tasks) == 2
    assert "Задачи из категории 'Работа' успешно удалены" in output

    inputs = iter(["Обучение", "нет"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    delete_task(tasks_manager, option="category")
    output = capsys.readouterr().out
    assert len(tasks_manager.tasks) == 2
    assert "Удаление задач отменено" in output

    inputs = iter(["   ", "Работа"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    delete_task(tasks_manager, option="category")
    output = capsys.readouterr().out
    assert len(tasks_manager.tasks) == 2
    assert "Категория не может быть пустой!" in output
    assert "Задачи из категории 'Работа' не найдены" in output


def test_search_tasks(tasks_manager, monkeypatch, capsys):
    """Тест функции поиска задач"""
    tasks_manager.add_task(
        title="Изучить Python",
        description="Пройти основы языка",
        category="Обучение",
        due_date="30.01.2025",
        priority="высокий"
    )
    tasks_manager.add_task(
        title="Пройти курс Django",
        description="Изучить основы Django",
        category="Работа",
        due_date="20.12.2024",
        priority="средний"
    )
    tasks_manager.add_task(
        title="Изучить Flask",
        description="Основы Flask",
        category="Обучение",
        due_date="01.01.2025",
        priority="низкий"
    )

    capsys.readouterr()
    monkeypatch.setattr("builtins.input", lambda _: "Python")
    search_tasks(tasks_manager, option="1")
    output = capsys.readouterr().out
    assert "Изучить Python" in output
    assert "Пройти курс Django" not in output

    monkeypatch.setattr("builtins.input", lambda _: "основы")
    search_tasks(tasks_manager, option="1")
    output = capsys.readouterr().out
    assert "Изучить Python" in output
    assert "Пройти курс Django" in output
    assert "Изучить Flask" in output

    monkeypatch.setattr("builtins.input", lambda _: "Работа")
    search_tasks(tasks_manager, option="2")
    output = capsys.readouterr().out
    assert "Пройти курс Django" in output
    assert "Изучить Python" not in output

    monkeypatch.setattr("builtins.input", lambda _: "выполнена")
    search_tasks(tasks_manager, option="3")
    output = capsys.readouterr().out
    assert "Задачи по заданному запросу не найдены" in output
