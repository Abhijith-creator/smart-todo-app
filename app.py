from flask import Flask, render_template, request, redirect, url_for
from todo_manager import load_tasks, add_task, update_task, delete_task
from notifier import run_scheduler_in_thread
from datetime import datetime

app = Flask(__name__)

run_scheduler_in_thread()

def format_deadline(date_str):
    """Convert '2025-10-22T19:40' → 'Thu Oct 02 2025'"""
    try:
        dt = datetime.strptime(date_str.replace("T", " "), "%Y-%m-%d %H:%M")
        return dt.strftime("%a %b %d %Y")
    except:
        return date_str

@app.route("/", methods=["GET", "POST"])
def index():
    tasks = load_tasks()
    for task in tasks:
        task["formatted_deadline"] = format_deadline(task["deadline"])

    if request.method == "POST":
        title = request.form.get("title")
        deadline = request.form.get("deadline")
        priority = request.form.get("priority")
        if title and deadline and priority:
            add_task(title, deadline, priority)
        return redirect(url_for("index"))

    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:index>")
def delete(index):
    delete_task(index)
    return redirect(url_for("index"))

@app.route("/complete/<int:index>")
def complete(index):
    update_task(index, completed=True)
    return redirect(url_for("index"))

@app.route("/update/<int:index>", methods=["GET", "POST"])
def update(index):
    tasks = load_tasks()
    task = tasks[index]

    if request.method == "POST":
        title = request.form.get("title")
        deadline = request.form.get("deadline")
        priority = request.form.get("priority")
        update_task(index, title, deadline, priority)
        return redirect(url_for("index"))

    task["formatted_deadline"] = format_deadline(task["deadline"])
    return render_template("update.html", task=task, index=index)

if __name__ == "__main__":
    app.run(debug=True)
