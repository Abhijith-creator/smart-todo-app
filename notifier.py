import schedule
import time
from datetime import datetime
from todo_manager import load_tasks
from plyer import notification
from threading import Thread

REMINDER_MINUTES = 10
notified_tasks = set()

def notify_task(task, pre_deadline=False):
    when = f"{REMINDER_MINUTES} minutes before" if pre_deadline else f"due on {task['deadline']}"
    message = f"Task '{task['title']}' is {when}!"
    print(f"⚠️ {message}")  # console log
    notification.notify(
        title="Smart To-Do Reminder",
        message=message,
        timeout=10
    )

def check_due_tasks():
    tasks = load_tasks()
    now = datetime.now()
    for idx, task in enumerate(tasks):
        if not task['completed']:
            deadline = datetime.strptime(task['deadline'], "%Y-%m-%d %H:%M")
            # Notify at deadline
            if now >= deadline and idx not in notified_tasks:
                notify_task(task)
                notified_tasks.add(idx)
            # Notify REMINDER_MINUTES before deadline
            elif 0 <= (deadline - now).total_seconds() <= REMINDER_MINUTES * 60 and idx not in notified_tasks:
                notify_task(task, pre_deadline=True)
                notified_tasks.add(idx)

def start_scheduler():
    schedule.every(1).minutes.do(check_due_tasks)
    print(f"🔔 Scheduler started. Notifications {REMINDER_MINUTES} minutes before deadlines.")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_scheduler_in_thread():
    thread = Thread(target=start_scheduler, daemon=True)
    thread.start()
