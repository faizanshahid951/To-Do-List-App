from dataclasses import dataclass, asdict
from datetime import datetime
import uuid
from typing import Optional

@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "Medium"  # Low, Medium, High
    category: str = "General" # Work, Personal, Shopping, etc.
    due_date: Optional[str] = None # Format: YYYY-MM-DD
    created_at: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", "").strip(),
            description=data.get("description", "").strip(),
            completed=bool(data.get("completed", False)),
            priority=data.get("priority", "Medium"),
            category=data.get("category", "General"),
            due_date=data.get("due_date"),
            created_at=data.get("created_at", datetime.now().isoformat())
        )
