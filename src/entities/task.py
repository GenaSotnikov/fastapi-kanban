from enum import Enum

class TaskStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task:
    id: str
    name: str
    description: str
    status: TaskStatus
    board_id: str
