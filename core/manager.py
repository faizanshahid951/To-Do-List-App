import json
import os
import threading
from typing import List, Optional
from .models import Task

class TaskManager:
    def __init__(self, storage_path: str = "data/tasks.json"):
        self.storage_path = storage_path
        self._lock = threading.Lock()
        self._ensure_storage()

    def _ensure_storage(self):
        dirname = os.path.dirname(self.storage_path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    def _load_tasks(self) -> List[Task]:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                return [Task.from_dict(item) for item in raw_data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_tasks(self, tasks: List[Task]):
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=2)

    def get_all(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = "created_desc"
    ) -> List[Task]:
        with self._lock:
            tasks = self._load_tasks()

        # Status filter: "all", "active", "completed"
        if status == "active":
            tasks = [t for t in tasks if not t.completed]
        elif status == "completed":
            tasks = [t for t in tasks if t.completed]

        # Priority filter
        if priority and priority != "all":
            tasks = [t for t in tasks if t.priority.lower() == priority.lower()]

        # Category filter
        if category and category != "all":
            tasks = [t for t in tasks if t.category.lower() == category.lower()]

        # Search query
        if search:
            query = search.strip().lower()
            tasks = [
                t for t in tasks
                if query in t.title.lower() or query in t.description.lower() or query in t.category.lower()
            ]

        # Sorting
        priority_map = {"High": 3, "Medium": 2, "Low": 1}
        if sort_by == "created_desc":
            tasks.sort(key=lambda t: t.created_at or "", reverse=True)
        elif sort_by == "created_asc":
            tasks.sort(key=lambda t: t.created_at or "")
        elif sort_by == "due_date":
            # Items without due_date go to the end
            tasks.sort(key=lambda t: (t.due_date is None or t.due_date == "", t.due_date or ""))
        elif sort_by == "priority":
            tasks.sort(key=lambda t: priority_map.get(t.priority, 0), reverse=True)

        return tasks

    def get_by_id(self, task_id: str) -> Optional[Task]:
        with self._lock:
            tasks = self._load_tasks()
            for task in tasks:
                if task.id == task_id:
                    return task
        return None

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "Medium",
        category: str = "General",
        due_date: Optional[str] = None
    ) -> Task:
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        new_task = Task(
            id="",
            title=title.strip(),
            description=description.strip(),
            completed=False,
            priority=priority if priority in ["Low", "Medium", "High"] else "Medium",
            category=category.strip() if category else "General",
            due_date=due_date if due_date else None
        )

        with self._lock:
            tasks = self._load_tasks()
            tasks.append(new_task)
            self._save_tasks(tasks)

        return new_task

    def update_task(self, task_id: str, updates: dict) -> Optional[Task]:
        with self._lock:
            tasks = self._load_tasks()
            updated_task = None
            for idx, task in enumerate(tasks):
                if task.id == task_id:
                    if "title" in updates:
                        if not updates["title"] or not updates["title"].strip():
                            raise ValueError("Task title cannot be empty")
                        task.title = updates["title"].strip()
                    if "description" in updates:
                        task.description = updates["description"].strip()
                    if "completed" in updates:
                        task.completed = bool(updates["completed"])
                    if "priority" in updates and updates["priority"] in ["Low", "Medium", "High"]:
                        task.priority = updates["priority"]
                    if "category" in updates:
                        task.category = updates["category"].strip() or "General"
                    if "due_date" in updates:
                        task.due_date = updates["due_date"] or None

                    tasks[idx] = task
                    updated_task = task
                    break

            if updated_task:
                self._save_tasks(tasks)
            return updated_task

    def toggle_task(self, task_id: str) -> Optional[Task]:
        with self._lock:
            tasks = self._load_tasks()
            toggled = None
            for idx, task in enumerate(tasks):
                if task.id == task_id:
                    task.completed = not task.completed
                    tasks[idx] = task
                    toggled = task
                    break
            if toggled:
                self._save_tasks(tasks)
            return toggled

    def delete_task(self, task_id: str) -> bool:
        with self._lock:
            tasks = self._load_tasks()
            initial_count = len(tasks)
            tasks = [t for t in tasks if t.id != task_id]
            if len(tasks) < initial_count:
                self._save_tasks(tasks)
                return True
            return False

    def clear_completed(self) -> int:
        with self._lock:
            tasks = self._load_tasks()
            initial_count = len(tasks)
            tasks = [t for t in tasks if not t.completed]
            cleared_count = initial_count - len(tasks)
            if cleared_count > 0:
                self._save_tasks(tasks)
            return cleared_count

    def get_stats(self) -> dict:
        with self._lock:
            tasks = self._load_tasks()
            total = len(tasks)
            completed = sum(1 for t in tasks if t.completed)
            active = total - completed
            categories = list({t.category for t in tasks if t.category})
            return {
                "total": total,
                "completed": completed,
                "active": active,
                "categories": sorted(categories)
            }
