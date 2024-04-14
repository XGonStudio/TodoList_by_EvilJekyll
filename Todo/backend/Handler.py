from datetime import datetime
import re

from backend.StorageManeger import StorageManager
from backend.ToDoList import ToDoList


class Handler:
    def __init__(self):
        self.todoList = None
        self.title_name = None

    def load_todo(self, filename) -> ToDoList:
        title, data = StorageManager.load(filename)
        self.todoList = ToDoList(title)
        self.todoList.load_info(data)
        return self.todoList.get_all_tasks()

    def save_todo(self, filename):
        if self.todoList is not None:
            StorageManager.save(self.todoList, filename)

    def get_task_list(self) -> list:
        return self.todoList.get_all_tasks()

    def add_task(self, name, sub: str, date):
        if self.todoList is None:
            self.todoList = ToDoList('ToDoList')
        subtasks = str(sub).split(';')

        # Валідація та перетворення дати
        date_format = '%d.%m.%Y'
        if date.strip():  # Якщо дата не порожня
            # Перевірка формату дати за допомогою регулярного виразу
            if re.match(r'^\d{1,2}[./-]\d{1,2}[./-]\d{4}$', date):
                # Якщо формат відповідає шаблону, перетворити в потрібний формат
                date_obj = datetime.strptime(date, '%d.%m.%Y').strftime(date_format)
                self.todoList.add_task(name, subtasks, date_obj)
            else:
                print("Неправильний формат дати. Використовуйте формат 'дд.мм.рррр'")
        else:
            # Якщо дата порожня, передати її без змін
            self.todoList.add_task(name, subtasks, date)


    def delete_task(self, task_id):
        self.todoList.delete_task(task_id)

    def edit_task(self, task_id, new_name, new_sub, new_deadline):
        new_sub = new_sub.split(';')
        self.todoList.edit_task(task_id, new_name, new_sub, new_deadline)