# TaskMaster - Django To-Do Application

A modern, responsive to-do list application built with Django and Tailwind CSS. Features comprehensive task management with priorities, categories and subtasks.

## ✨ Features

- **Task Management**: Create, edit, delete, and toggle completion
- **Priority Levels**: High, Medium, Low with color-coded badges
- **Categories**: Organize tasks with custom categories
- **Due Dates**: Set deadlines
- **Subtasks**: Break down complex tasks into manageable subtasks
- **Notes**: Add detailed notes and links to tasks
- **Bulk Actions**: Select multiple tasks for batch operations
- **Smart Filtering**: Filter by priority, category, status, and due date
- **Search**: Full-text search across task titles and descriptions
- **Progress Tracking**: Visual indicators for subtask completion

## 🛠️ Technology Stack

- **Backend**: Django 5.2
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Database**: SQLite

## 🚀 Quick Start

### Prerequisites
- Python 3.8+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sudip6164/django-todo-list.git
   cd django-todo-list
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run development server**
   ```bash
   python manage.py runserver
   ```

6. **Visit the application**
   ```
   http://localhost:8000
   ```

## 🎯 Usage

### Creating Tasks
1. Click "Add Task" in the sidebar
2. Fill in title, description, priority, category, and due date
3. Add notes or parent task as needed
4. Save to create the task

### Managing Tasks
- **Toggle Completion**: Click the checkmark icon
- **Edit**: Click the edit icon to modify task details
- **Delete**: Click the delete icon
- **Bulk Actions**: Select multiple tasks and use bulk action bar

### Filtering and Search
- Use the search bar for quick text search
- Apply filters for priority, category, status, and due date
- Combine multiple filters for precise results

## 📁 Project Structure
```
todo_project/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── todo_project/          # Django project settings package
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── todo/                  # Main app
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── context_processors.py
    ├── migrations/
    │   └── __init__.py
    ├── models.py
    ├── templates/
    │   └── todo/         
    │       ├── add.html
    │       ├── base.html
    │       ├── edit.html
    │       └── indexx.html
    ├── tests.py
    ├── urls.py
    └── views.py
```

## Screenshots

<img width="1349" height="608" alt="image" src="https://github.com/user-attachments/assets/f3475b2e-898f-46f3-b511-2b5075423779" />

<img width="1352" height="606" alt="image" src="https://github.com/user-attachments/assets/baf65d3c-707c-490b-b0f4-3df69b989a1e" />

<img width="1352" height="552" alt="image" src="https://github.com/user-attachments/assets/5eb2cdc7-0a19-4fdb-894c-d98f0d24af07" />

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with Django and Tailwind CSS**
