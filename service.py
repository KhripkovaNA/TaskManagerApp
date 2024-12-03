from datetime import datetime
from typing import Dict
from task_manager import TaskManager


def list_tasks(tasks_manager: TaskManager, option: str) -> None:
    category = None
    if option == "2" and tasks_manager.tasks:
        while True:
            category = input("Введите категорию задачи или введите 'отмена' для возврата в основное меню: ").strip()

            if category.lower() == "отмена":
                print("Просмотр задач отменен")
                return

            if not category:
                print("Введена пустая строка!")
                continue

            break

    tasks_manager.list_tasks(category)


def add_task(tasks_manager: TaskManager) -> None:
    print("Введите все поля новой задачи или введите 'отмена' на любом этапе для возврата в основное меню")
    new_task_dict = {"title": None, "description": None, "category": None, "due_date": None, "priority": None}
    input_list = ["Название задачи", "Описание задачи", "Категория задачи",
                  "Срок выполнения (дд.мм.гггг)", "Приоритет задачи (низкий/средний/высокий)"]

    for task_option, input_str in zip(new_task_dict.keys(), input_list):
        while True:
            user_input = input(f"{input_str}: ").strip()

            if user_input.lower() == "отмена":
                print("Добавление задачи отменено")
                return

            if not user_input:
                print("Введена пустая строка!")
                continue

            # Проверка и обработка данных
            if task_option == "due_date":
                try:
                    new_task_dict[task_option] = datetime.strptime(user_input, "%d.%m.%Y").date()
                except ValueError:
                    print("Некорректный формат даты! Используйте формат дд.мм.гггг")
                    continue
            elif task_option == "priority":
                if user_input.lower() not in ["низкий", "средний", "высокий"]:
                    print("Некорректный приоритет задачи! Используйте: низкий, средний или высокий")
                    continue
                new_task_dict[task_option] = user_input.lower()
            else:
                new_task_dict[task_option] = user_input

            break  # Переход к следующему полю

    # Убедимся, что все данные заполнены
    if None in new_task_dict.values():
        print("Не удалось создать задачу")
        return

    new_task_dict["due_date"] = f"{new_task_dict["due_date"]:%d.%m.%Y}"
    tasks_manager.add_task(**new_task_dict)


def edit_task_by_field() -> Dict:
    field_map = {"1": {"name": "title", "meaning": "название", "input_str": "Введите новое название задачи"},
                 "2": {"name": "description", "meaning": "описание", "input_str": "Введите новое описание задачи"},
                 "3": {"name": "category", "meaning": "категория", "input_str": "Введите новую категорию задачи"},
                 "4": {"name": "due_date", "meaning": "срок выполнения",
                       "input_str": "Введите новый срок исполнения задачи"},
                 "5": {"name": "priority", "meaning": "приоритет", "input_str": "Введите новый приоритет задачи"}}
    edit_dict = {}
    while field_map:
        print("Выберите поле для редактирования или введите 'отмена' для возврата в основное меню")
        fields_to_edit = ", ".join([f"{key} - {value['meaning']}" for key, value in field_map.items()])
        field = input(f"{fields_to_edit}: ").strip()

        if field.lower() == "отмена":
            print("Редактирование задачи отменено")
            break

        if field not in field_map:
            print("Некорректное поле для редактирования!")
            continue

        field_data = field_map[field]
        new_field = input(f"{field_data['input_str']} или введите 'отмена': ").strip()

        if new_field.lower() == "отмена":
            print(f"Редактирование поля '{field_data['meaning']}' отменено")
            continue

        if not new_field:
            print("Поле не может быть пустым! Редактирование поля '{field_data['meaning']}' отменено")
            continue

        # Обработка специфичных полей
        if field == "4":  # Дата выполнения
            try:
                new_field = f"{datetime.strptime(new_field, '%d.%m.%Y').date():%d.%m.%Y}"
            except ValueError:
                print(f"Некорректный формат даты! Редактирование поля '{field_data['meaning']}' отменено")
                continue

        elif field == "5":  # Приоритет
            if new_field.lower() not in ["низкий", "средний", "высокий"]:
                print(f"Некорректный приоритет! Редактирование поля '{field_data['meaning']}' отменено")
                continue
            new_field = new_field.lower()

        # Сохранение нового значения
        edit_dict[field_data["name"]] = new_field
        del field_map[field]  # Удаляем обработанное поле

        if field_map:
            continue_edit = input(
                "Введите 'да', чтобы завершить редактирование задачи, или нажмите Enter для продолжения: ").strip()
            if continue_edit.lower() == "да":
                break

    return edit_dict


def edit_task(tasks_manager: TaskManager) -> None:
    while True:
        user_input = input("Введите ID задачи для редактирования или 'отмена' для возврата в основное меню: ").strip()
        if user_input.lower() == "отмена":
            print("Редактирование задачи отменено")
            return
        try:
            task_id = int(user_input)
            if task_id <= 0:
                print("Некорректный ID! ID должно быть положительным числом")
                continue
        except ValueError:
            print("Некорректный ID! Введите число")
            continue

        task = tasks_manager.get_task(task_id)
        if not task:
            print(f"Задача с ID {task_id} не найдена")
            continue

        print("Текущие данные задачи:")
        print(task.present_task())

        updated_fields = edit_task_by_field()
        if updated_fields:
            tasks_manager.edit_task(task_id, **updated_fields)
            return
        else:
            print("Редактирование задачи отменено")
            return


def update_status(tasks_manager: TaskManager) -> None:
    while True:
        user_input = input("Введите ID задачи для изменения статуса или введите 'отмена' для возврата в основное меню: ")
        if user_input.lower() == "отмена":
            print("Изменение статуса отменено")
            return
        try:
            task_id = int(user_input)
            if task_id <= 0:
                print("Некорректный ID! ID должно быть положительным числом")
                continue
        except ValueError:
            print("Некорректный ID! Введите число")
            continue
        tasks_manager.update_status(task_id)
        return


def delete_task(tasks_manager: TaskManager, option: str) -> None:
    del_options = {}
    while True:
        if option == "id":
            user_input = input("Введите ID задачи для удаления или введите 'отмена' для возврата в основное меню: ")
            if user_input.lower() == "отмена":
                print("Изменение статуса отменено")
                return
            try:
                task_id = int(user_input)
                if task_id <= 0:
                    print("Некорректный ID! ID должно быть положительным числом")
                    continue
            except ValueError:
                print("Некорректный ID! Введите число")
                continue
            del_options["task_id"] = int(user_input)

        else:
            category = input("Введите категорию для удаления задач или введите "
                             "'отмена' для возврата в основное меню: ").strip()
            if category.lower() == "отмена":
                print("Редактирование задачи отменено")
                return
            if not category:
                print("Категория не может быть пустой!")
                continue
            del_options["category"] = category

        tasks_manager.delete_tasks(**del_options)
        return


def search_tasks(tasks_manager: TaskManager, option: str) -> None:
    search_dict = {}
    option_dict = {"1": {"search_key": "keyword", "input_str": "Введите ключевое слово"},
                   "2": {"search_key": "category", "input_str": "Введите категорию"},
                   "3": {"search_key": "status", "input_str": "Введите статус (выполнена/не выполнена)"}}

    option_data = option_dict[option]
    while True:
        search_option = input(f"{option_data['input_str']} или введите 'отмена' для возврата в основное меню: ").strip()

        if search_option == "отмена":
            print("Поиск задач отменен")
            return

        if not search_option:
            print("Не указаны критерии для поиска задач")
            continue

        if option_data["search_key"] == "status" and search_option not in ["выполнена", "не выполнена"]:
            print("Некорректный статус для поиска!")
            continue

        search_dict[option_data["search_key"]] = search_option
        tasks_manager.search_tasks(**search_dict)
