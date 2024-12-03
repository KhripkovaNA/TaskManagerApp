from service import add_task, edit_task, update_status, delete_task, search_tasks, list_tasks
from task_manager import TaskManager

FILENAME = "tasks.json"


def main():
    tasks_manager = TaskManager(FILENAME)
    while True:
        print("\nМеню:")
        print("1. Просмотр задач")
        print("2. Добавление задачи")
        print("3. Изменение задачи")
        print("4. Удаление задачи")
        print("5. Поиск задач")
        print("6. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":  # Просмотр задач
            while True:
                print("\n1. Просмотр всех задач")
                print("2. Просмотр задач по категориям")
                print("3. Возврат в основное меню")
                sub_choice = input("Выберите поддействие: ")

                if sub_choice in ["1", "2"]:  # Просмотр всех текущих задач или задач по категориям
                    list_tasks(tasks_manager, sub_choice)
                elif sub_choice == "3":  # Возврат в основное меню
                    print("Возврат в основное меню...")
                    break
                else:
                    print("Неверный выбор поддействия!")

        elif choice == "2":  # Добавление задачи
            add_task(tasks_manager)

        elif choice == "3":  # Изменение задачи
            while True:
                print("\n1. Редактирование задачи")
                print("2. Отметка задачи как выполненной")
                print("3. Возврат в основное меню")
                sub_choice = input("Выберите поддействие: ")

                if sub_choice == "1":  # Редактирование задачи
                    edit_task(tasks_manager)
                elif sub_choice == "2":  # Изменение статуса задачи
                    update_status(tasks_manager)
                elif sub_choice == "3":  # Возврат в основное меню
                    print("Возврат в основное меню...")
                    break
                else:
                    print("Неверный выбор поддействия!")

        elif choice == "4":  # Удаление задачи
            while True:
                print("\n1. Удаление задачи по ID")
                print("2. Удаление задач по категории")
                print("3. Возврат в основное меню")
                sub_choice = input("Выберите поддействие: ")

                if sub_choice == "1":  # Удаление задачи по ID
                    delete_task(tasks_manager, option="id")
                elif sub_choice == "2":  # Удаление задач по категории
                    delete_task(tasks_manager, option="category")
                elif sub_choice == "3":  # Возврат в основное меню
                    print("Возврат в основное меню...")
                    break
                else:
                    print("Неверный выбор поддействия!")

        elif choice == "5":  # Поиск задач
            while True:
                print("\n1. Поиск по ключевым словам")
                print("2. Поиск по категории")
                print("3. Поиск по статусу выполнения")
                print("4. Возврат в основное меню")
                sub_choice = input("Выберите поддействие: ")

                if sub_choice in ["1", "2", "3"]:  # Поиск по ключевым словам, категории или статусу
                    search_tasks(tasks_manager, option=sub_choice)
                elif sub_choice == "4":  # Возврат в основное меню
                    print("Возврат в основное меню...")
                    break
                else:
                    print("Неверный выбор поддействия!")

        elif choice == "6":  # Выход
            print("Завершение работы")
            break

        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()
