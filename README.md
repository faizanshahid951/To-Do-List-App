# TaskMaster: Python To-Do List Web App

A clean, responsive, and persistent To-Do List web application built using **Python (Flask)** and **Tailwind CSS**, featuring local JSON persistence.

---

## Features
- **Task Management**:
  - Add tasks with Title, Description, Priority (Low, Medium, High), Category/Tag, and Due Date.
  - Complete / Toggle task completion status with instant visual feedback.
  - Edit existing tasks via an edit modal.
  - Delete individual tasks.
  - Bulk clear completed tasks.
- **Search, Filter & Sort**:
  - Filter by status (**All**, **Active**, **Completed**).
  - Filter by **Category** (dynamically updated).
  - Filter by **Priority** (High, Medium, Low).
  - Live **Search** by keywords (title, description, category).
  - Sort by **Newest First**, **Oldest First**, **Due Date**, or **Priority**.
- **Persistence**:
  - All tasks are safely stored locally in `data/tasks.json` across app restarts.
- **Responsive UI**:
  - Modern card-based dashboard with responsive layout for desktop and mobile.

---

## Project Structure
```text
To-Do List App/
├── app.py                 # Flask server and REST API endpoints
├── requirements.txt       # Dependencies
├── core/
│   ├── models.py          # Task data model
│   └── manager.py         # Task business logic & JSON persistence
├── templates/
│   └── index.html         # Web dashboard UI
├── static/
│   ├── css/style.css      # Custom styles
│   └── js/app.js          # Client-side controller (Fetch API)
├── tests/
│   ├── test_manager.py    # Unit tests for manager logic
│   └── test_api.py        # Integration tests for REST API
└── data/
    └── tasks.json         # Local data store (auto-created)
```

---

## Getting Started

### 1. Prerequisites
- Python 3.9+ installed.

### 2. Setup Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python3 app.py
```

Open your web browser and go to:
```
http://127.0.0.1:8080
```

---

## Running Tests
Run the automated test suite with:
```bash
python3 -m unittest discover tests
```
