from enum import Enum as PyEnum

class TaskPriorityEnum(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatusEnum(str, PyEnum):
    TO_DO = "to_do"
    IN_PROGRESS = "in_progress"
    TESTING = "testing"
    DONE = "done"


class ProjectVisibilityEnum(str, PyEnum):
    PRIVATE = "private"
    TEAM = "team"
    PUBLIC = "public"
