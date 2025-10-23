import json
from datetime import datetime

DB_FILE = "database.json"

def load_tasks():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_tasks(tasks):
    with open(DB_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(title, deadline, priority):
    tasks = load_tasks()
    tasks.append({
        "title": title,
        "deadline": deadline,
        "priority": priority,
        "completed": False
    })
    save_tasks(tasks)

def update_task(index, title=None, deadline=None, priority=None, completed=None):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        if title: tasks[index]['title'] = title
        if deadline: tasks[index]['deadline'] = deadline
        if priority: tasks[index]['priority'] = priority
        if completed is not None: tasks[index]['completed'] = completed
        save_tasks(tasks)

def delete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
