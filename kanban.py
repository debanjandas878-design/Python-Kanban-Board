
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import json
import os
from datetime import datetime, date
import calendar

root = tk.Tk()
root.title("Kanban Task Manager")
root.geometry("1200x780")
root.configure(bg="#F4F6F9")

FILE = "tasks.json"

columns = ["TO DO", "IN PROGRESS", "DONE"]
colors = ["#E8F0FE", "#FFF3D6", "#DDF5E5"]

priorities = ["High", "Medium", "Low"]

priority_colors = {
    "High": "#FFCCCC",
    "Medium": "#FFE6B3",
    "Low": "#D9F2E6"
}

tasks = []
def update_task_status(task, new_status):
    task["status"] = new_status

    if new_status == "DONE":
        task["completion_date"] = date.today().strftime("%Y-%m-%d")
    else:
        task["completion_date"] = ""

    save_tasks()
    refresh_board()

# Load tasks
def load_tasks():
    global tasks

    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as file:
                tasks = json.load(file)
        except (json.JSONDecodeError, OSError):
            tasks = []

    for task in tasks:
        task.setdefault("priority", "Medium")
        task.setdefault("due_date", "")
        task.setdefault("completion_date", "")



# Save tasks
def save_tasks():
    with open(FILE, "w") as file:
        json.dump(tasks, file, indent=4)


# Heading
tk.Label(
    root,
    text="MY KANBAN BOARD",
    font=("Arial", 25, "bold"),
    bg="#F4F6F9",
    fg="#243447"
).pack(pady=12)


# Dashboard
dashboard = tk.Frame(root, bg="#F4F6F9")
dashboard.pack(pady=5)

summary_label = tk.Label(
    dashboard,
    font=("Arial", 12, "bold"),
    bg="#F4F6F9",
    fg="#243447"
)
summary_label.pack()

# Progress tracker
progress_label = tk.Label(
    dashboard,
    text="Overall Progress: 0%",
    font=("Arial", 11, "bold"),
    bg="#F4F6F9"
)
progress_label.pack(pady=5)

progress_bar = ttk.Progressbar(
    dashboard,
    length=350,
    maximum=100,
    mode="determinate"
)
progress_bar.pack(pady=5)
summary_label.pack()


# Search bar
search_frame = tk.Frame(root, bg="#F4F6F9")
search_frame.pack(pady=12)

tk.Label(
    search_frame,
    text="Search Task:",
    font=("Arial", 11),
    bg="#F4F6F9"
).pack(side="left", padx=5)

search_var = tk.StringVar()
priority_filter = tk.StringVar(value="All Priorities")
due_filter = tk.StringVar(value="All Deadlines")



search_entry = tk.Entry(
    search_frame,
    textvariable=search_var,
    width=30,
    font=("Arial", 11)
)
search_entry.pack(side="left", padx=5)
# Priority Filter
priority_menu = tk.OptionMenu(
    search_frame,
    priority_filter,
    "All Priorities",
    "High",
    "Medium",
    "Low",
    command=lambda value: refresh_board()
)

priority_menu.pack(side="left", padx=10)
due_menu = tk.OptionMenu(
    search_frame,
    due_filter,
    "All Deadlines",
    "Due Today",
    "Next 7 Days",
    "Overdue",
    "No Deadline",
    command=lambda value: refresh_board()
)
due_menu.pack(side="left", padx=10)

# Board
board = tk.Frame(root, bg="#F4F6F9")
board.pack(fill="both", expand=True, padx=20, pady=10)

column_frames = {}
column_canvases = {}
counter_labels = {}

for i, column in enumerate(columns):

    frame = tk.Frame(board, bg=colors[i])
    frame.pack(side="left", fill="both", expand=True, padx=10)

    title = tk.Label(
        frame,
        text=column,
        font=("Arial", 15, "bold"),
        bg=colors[i]
    )
    title.pack(pady=10)

    counter = tk.Label(
        frame,
        text="Tasks: 0",
        font=("Arial", 10),
        bg=colors[i]
    )
    counter.pack()

    counter_labels[column] = counter

    # Scrollable canvas
    canvas = tk.Canvas(
        frame,
        bg=colors[i],
        highlightthickness=0
    )
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(
        frame,
        orient="vertical",
        command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = tk.Frame(canvas, bg=colors[i])

    window_id = canvas.create_window(
        (0, 0),
        window=inner_frame,
        anchor="nw"
    )

    def update_scroll(event, c=canvas):
        c.configure(scrollregion=c.bbox("all"))

    def update_width(event, c=canvas, w=window_id):
        c.itemconfigure(w, width=event.width)

    inner_frame.bind("<Configure>", update_scroll)
    canvas.bind("<Configure>", update_width)

    column_frames[column] = inner_frame
    column_canvases[column] = canvas


# Refresh board
def refresh_board():

    query = search_var.get().strip().lower()
    selected_priority = priority_filter.get()
    selected_due = due_filter.get()

    for column in columns:
        for widget in column_frames[column].winfo_children():
            widget.destroy()

    for column in columns:

        column_tasks = [
            task for task in tasks
            if task["status"] == column
        ]

        counter_labels[column].config(
            text=f"Tasks: {len(column_tasks)}"
        )

        for task in column_tasks:

            # Text search
            if query and query not in task["title"].lower():
                continue

            # Priority filter
            if selected_priority != "All Priorities":
                if task.get("priority", "Medium") != selected_priority:
                    continue

            # Due date filter
            due_date = task.get("due_date", "")

            if selected_due == "No Deadline":
                if due_date:
                    continue

            elif selected_due != "All Deadlines":

                if not due_date:
                    continue

                deadline = datetime.strptime(
                    due_date, "%Y-%m-%d"
                ).date()

                today = date.today()

                if selected_due == "Due Today":
                    if deadline != today:
                        continue

                elif selected_due == "Next 7 Days":
                    if not (today <= deadline <= date.fromordinal(today.toordinal() + 7)):
                        continue

                elif selected_due == "Overdue":
                    if deadline >= today:
                        continue

            create_task_card(task)

    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task["status"] == "DONE"
    )

    summary_label.config(
        text=f"Total Tasks: {total}    |    Completed: {completed}"
    )

    pending = total - completed

    percentage = (
        (completed / total) * 100
        if total > 0 else 0
    )

    progress_label.config(
        text=f"Overall Progress: {percentage:.1f}% | Pending: {pending}"
    )

    progress_bar["value"] = percentage


# Create task card
# Create task card
def create_task_card(task):

    status = task["status"]

    card = tk.Frame(
        column_frames[status],
        bg="white",
        bd=1,
        relief="solid"
    )
    card.pack(fill="x", padx=10, pady=7)

    # Task title
    tk.Label(
        card,
        text=task["title"],
        bg="white",
        font=("Arial", 11, "bold"),
        wraplength=230
    ).pack(pady=7)
    # Due date
    due_date = task.get("due_date", "")

    if due_date:
        deadline_color = "#333333"

        if status != "DONE":
            deadline = datetime.strptime(
                due_date, "%Y-%m-%d"
            ).date()

            if deadline < date.today():
                deadline_color = "#E53935"

        tk.Label(
            card,
            text=f"Due: {due_date}",
            bg="white",
            fg=deadline_color,
            font=("Arial", 9, "bold")
        ).pack(pady=3)
    else:
        tk.Label(
            card,
            text="No deadline",
            bg="white",
            fg="#888888",
            font=("Arial", 9)
        ).pack(pady=3)

    # Priority
    priority = task.get("priority", "Medium")

    tk.Label(
        card,
        text=f"Priority: {priority}",
        bg=priority_colors[priority],
        font=("Arial", 9, "bold")
    ).pack(pady=3)

    priority_var = tk.StringVar(value=priority)

    tk.OptionMenu(
        card,
        priority_var,
        *priorities,
        command=lambda value: change_priority(task, value)
    ).pack(pady=2)

    # Move task
    status_var = tk.StringVar(value=status)

    tk.OptionMenu(
        card,
        status_var,
        *columns,
        command=lambda value: move_task(task, value)
    ).pack(pady=2)

    # Edit button
    tk.Button(
        card,
        text="Edit",
        command=lambda: edit_task(task)
    ).pack(pady=2)
    # Set Deadline button
    tk.Button(
        card,
        text="Set Deadline",
        command=lambda: set_deadline(task)
    ).pack(pady=2)

    # Delete button
    tk.Button(
        card,
        text="Delete",
        command=lambda: delete_task(task)
    ).pack(pady=2)




# Add task
def add_task():

    title = simpledialog.askstring(
        "New Task",
        "Enter your task:"
    )

    if title and title.strip():

        due_date = simpledialog.askstring(
            "Due Date",
            "Enter deadline (YYYY-MM-DD):"
        )

        if not due_date:
            return

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Enter date as YYYY-MM-DD."
            )
            return

        tasks.append({
            "title": title.strip(),
            "status": "TO DO",
            "priority": "Medium",
            "due_date": due_date
        })

        save_tasks()
        refresh_board()



# Edit task
def edit_task(task):

    new_title = simpledialog.askstring(
        "Edit Task",
        "Enter new task name:",
        initialvalue=task["title"]
    )

    if new_title and new_title.strip():

        task["title"] = new_title.strip()
        save_tasks()
        refresh_board()

        # Set or update deadline
def set_deadline(task):

    due_date = simpledialog.askstring(
        "Set Deadline",
        "Enter deadline (YYYY-MM-DD):",
        initialvalue=task.get("due_date", "")
    )

    if not due_date:
        return

    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror(
            "Invalid Date",
            "Enter date as YYYY-MM-DD."
        )
        return

    task["due_date"] = due_date
    save_tasks()
    refresh_board()


# Change priority
def change_priority(task, priority):

    task["priority"] = priority
    save_tasks()
    refresh_board()


# Move task
def move_task(task, new_status):

    task["status"] = new_status
    save_tasks()
    refresh_board()


# Delete task
def delete_task(task):

    if messagebox.askyesno(
        "Delete Task",
        "Delete this task?"
    ):
        tasks.remove(task)
        save_tasks()
        refresh_board()


# Search automatically
search_var.trace_add(
    "write",
    lambda *args: refresh_board()
)

# Calendar View Button
def open_calendar():
    # Calendar View


    calendar_window = tk.Toplevel(root)
    calendar_window.title("Task Calendar")
    calendar_window.geometry("650x650")
    calendar_window.configure(bg="#F4F6F9")

    # Current month and year
    today = date.today()
    current = [today.year, today.month]

    # Calendar heading
    month_label = tk.Label(
        calendar_window,
        font=("Arial", 18, "bold"),
        bg="#F4F6F9",
        fg="#243447"
    )
    month_label.pack(pady=15)

    # Month navigation
    navigation = tk.Frame(
        calendar_window,
        bg="#F4F6F9"
    )
    navigation.pack(pady=5)

    # Calendar grid
    calendar_frame = tk.Frame(
        calendar_window,
        bg="#F4F6F9"
    )
    calendar_frame.pack(pady=10)

    # Selected date heading
    selected_label = tk.Label(
        calendar_window,
        text="Select a date to see its tasks",
        font=("Arial", 12, "bold"),
        bg="#F4F6F9"
    )
    selected_label.pack(pady=10)

    # Task list
    task_list = tk.Listbox(
        calendar_window,
        width=55,
        height=8,
        font=("Arial", 10)
    )
    task_list.pack(pady=10)

    # Show tasks for selected date
    def show_tasks(day):

        selected_date = date(
            current[0],
            current[1],
            day
        )

        selected_label.config(
            text=f"Tasks due on {selected_date.strftime('%d %B %Y')}"
        )

        task_list.delete(0, tk.END)

        found = False

        for task in tasks:
            if task.get("due_date", "") == selected_date.strftime("%Y-%m-%d"):

                task_list.insert(
                    tk.END,
                    f"{task['title']} ({task['status']})"
                )

                found = True

        if not found:
            task_list.insert(
                tk.END,
                "No tasks due on this date."
            )

    # Draw calendar
    def draw_calendar():

        for widget in calendar_frame.winfo_children():
            widget.destroy()

        year = current[0]
        month = current[1]

        month_label.config(
            text=f"{calendar.month_name[month]} {year}"
        )

        # Weekday headings
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for col, day_name in enumerate(weekdays):
            tk.Label(
                calendar_frame,
                text=day_name,
                font=("Arial", 10, "bold"),
                bg="#E8F0FE",
                width=9,
                pady=8
            ).grid(row=0, column=col, padx=2, pady=2)

        weeks = calendar.monthcalendar(year, month)

        for row, week in enumerate(weeks, start=1):

            for col, day in enumerate(week):

                if day == 0:
                    continue

                date_text = date(
                    year, month, day
                ).strftime("%Y-%m-%d")

                has_task = any(
                    task.get("due_date", "") == date_text
                    for task in tasks
                )

                button_color = "#DCE8FF" if has_task else "white"

                tk.Button(
                    calendar_frame,
                    text=str(day),
                    width=9,
                    height=2,
                    bg=button_color,
                    command=lambda d=day: show_tasks(d)
                ).grid(
                    row=row,
                    column=col,
                    padx=2,
                    pady=2
                )

    # Previous month
    def previous_month():

        current[1] -= 1

        if current[1] == 0:
            current[1] = 12
            current[0] -= 1

        draw_calendar()

    # Next month
    def next_month():

        current[1] += 1

        if current[1] == 13:
            current[1] = 1
            current[0] += 1

        draw_calendar()

    tk.Button(
        navigation,
        text="◀ Previous",
        command=previous_month
    ).pack(side="left", padx=15)

    tk.Button(
        navigation,
        text="Next ▶",
        command=next_month
    ).pack(side="left", padx=15)

    draw_calendar()
#Search automatically
search_var.trace_add(
    "write",
    lambda *args: refresh_board()
)
tk.Button(
    root,
    text="📅 CALENDAR VIEW",
    font=("Arial", 11, "bold"),
    bg="#E8F0FE",
    fg="#243447",
    command=open_calendar,
    padx=15,
    pady=7
).pack(pady=5)

# Add task button
tk.Button(
    root,
    text="+ ADD NEW TASK",
    font=("Arial", 12, "bold"),
    bg="#315EFB",
    fg="white",
    command=add_task,
    padx=20,
    pady=8
).pack(pady=10)


# Start application
load_tasks()
refresh_board()

root.mainloop()