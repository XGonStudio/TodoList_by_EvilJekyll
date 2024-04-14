from datetime import datetime


class ToDoList:
    def __init__(self, todolist_title: str):
        self.__todolist_title = todolist_title
        self.__list_of_tasks = []
        self.id = len(self.__list_of_tasks)

    def get_title(self):
        return self.__todolist_title

    def set_title(self, todolist_title: str):
        self.__todolist_title = todolist_title

    def __id_generator(self):
        self.id += 1
        return self.id

    def add_task(self, task_text: str, sub_tasks, deadline = None):
        task_id = self.__id_generator()

        if task_text == '':
            task_text = f'Завдання №{task_id}'

        new_task = {
            'id': task_id,
            'task_create_time': datetime.now().strftime('%d/%m/%Y'),
            'task_text': task_text,
            'sub_tasks': list(sub_tasks),
            'is_done': False,
            'deadline': deadline
        }
        self.__list_of_tasks.append(new_task)

    def delete_task(self, task_id):
        for task in self.__list_of_tasks:
            if task['id'] == task_id:
                index = self.__list_of_tasks.index(task)
                del self.__list_of_tasks[index]
        self.id = len(self.__list_of_tasks)
        for task in self.__list_of_tasks:
            if task['id'] > task_id:
                task['id'] -= 1

    def get_all_tasks(self):
        return self.__list_of_tasks

    def load_info(self, task_list):
        self.__list_of_tasks = task_list

    def edit_task(self, task_id, task_text, sub_tasks, deadline):
        for task in self.__list_of_tasks:
            if task['id'] == task_id:
                task['task_text'] = task_text
                task['sub_tasks'] = sub_tasks
                task['deadline'] = deadline