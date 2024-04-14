import json
from backend.ToDoList import ToDoList


class StorageManager:
    @staticmethod
    def save(list_ex: 'ToDoList', filename: str) -> str:
        data = list_ex.get_all_tasks()

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        return f"Todolist {list_ex.get_title()} saved to: {filename}"

    @staticmethod
    def load(filename: str) -> tuple:
        with open(filename, 'r') as f:
            data = json.load(f)
            return filename, data
