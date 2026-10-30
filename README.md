# Python-Kanban-Board
A python based kanban board project:

📋 Kanban Task Manager

A desktop-based task management application built using Python and Tkinter. This application helps users organize, manage, track and prioritize their daily tasks through a simple and interactive Kanban board.

📌 About the Project

The Kanban Task Manager is a Python GUI application designed to make task management easier and more organized.

It follows the Kanban workflow, where tasks are divided into three stages:

- TO DO: Tasks that are yet to be started.
- IN PROGRESS: Tasks that are currently being worked on.
- DONE: Tasks that have been successfully completed.

Users can create tasks, update their details, assign priorities, set deadlines and track their overall progress through a user-friendly dashboard.

The application also includes a calendar view and JSON-based data storage to make task management more convenient.

✨ Features

1. Task Management

- Add new tasks.
- Edit existing task titles.
- Delete tasks.
- Move tasks between different Kanban stages.

2. Priority Management

- Assign priorities to tasks:
  - High
  - Medium
  - Low
- Identify important tasks using colour-coded priority labels.

3. Deadline Management

- Set deadlines while creating tasks.
- Add or update deadlines for existing tasks.
- Display deadlines on task cards.
- Highlight overdue tasks.

4. Search Functionality

- Search for tasks by their titles.
- Automatically update the displayed tasks while typing.

5. Task Filtering

Filter tasks according to:

- Priority: All, High, Medium and Low.
- Deadline: All Deadlines, Due Today, Next 7 Days, Overdue and No Deadline.

6. Dashboard and Progress Tracking

- Display the total number of tasks.
- Display the number of completed tasks.
- Track overall task completion progress.
- View progress through a progress bar.

7. Calendar View

- Display a monthly calendar.
- Navigate between previous and next months.
- Highlight dates that have scheduled tasks.
- Select a date to view the tasks due on that date.

8. Data Persistence

- Store task information in a JSON file.
- Automatically save changes.
- Load previously saved tasks when the application starts.

9. Scrollable Kanban Columns

- Navigate through task cards using scrollable columns.
- Manage multiple tasks without overcrowding the interface.

🛠️ Technologies Used

Technology| Purpose
Python| Main programming language
Tkinter| Graphical User Interface
JSON| Storing task information
datetime| Managing deadlines and dates
calendar| Generating the monthly calendar
VS Code| Development environment

📂 Project Structure

Kanban_Board/
│
├── kanban.py
│
├── tasks.json
│
└── README.md

File descriptions:

- "kanban.py" – Main Python source code containing the application logic and GUI.
- "tasks.json" – Stores task information and preserves data between sessions.
- "README.md" – Documentation describing the project, its features and usage.

Note: The JSON file is generated when the application saves task data.

⚙️ Installation and Setup

Prerequisites

- Python 3.x installed on your system.
- Visual Studio Code or another Python-compatible editor.

Step 1: Clone the Repository

git clone YOUR_REPOSITORY_URL

Step 2: Navigate to the Project Directory

cd Kanban_Board

Step 3: Run the Application

python kanban.py

The application window will open, and you can start managing your tasks.

📖 How to Use

1. Launch the application.
2. Click the Add Task button to create a new task.
3. Assign a priority and deadline.
4. Move tasks between TO DO, IN PROGRESS and DONE.
5. Use the search bar to find specific tasks.
6. Apply filters to organize your task list.
7. Use the calendar view to check upcoming deadlines.
8. Monitor your progress through the dashboard.

Your tasks are saved automatically in the JSON file.

🎯 Project Objectives

- To understand Python GUI development using Tkinter.
- To implement CRUD operations (Create, Read, Update and Delete).
- To understand file handling and JSON data storage.
- To implement date and deadline management.
- To develop problem-solving and programming skills.
- To create a practical productivity application.

🚀 Future Improvements

Some possible enhancements for future versions include:

- Responsive layout for different window sizes.
- Keyboard shortcuts and improved keyboard accessibility.
- Advanced analytics and graphical reports.
- Task descriptions and notes.
- Exporting task information to CSV.
- User authentication and multiple-user support.

👩‍💻 Project Information

Project Name: Kanban Task Manager

Project Type: Desktop Application

Programming Language: Python

GUI Framework: Tkinter

Storage: JSON

Development Environment: Visual Studio Code

📜 License

This project is created for educational and learning purposes. You may modify and improve it as needed.
