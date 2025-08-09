from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.enums import ProjectVisibilityEnum, TaskPriorityEnum, TaskStatusEnum, UserRoleEnum

#User
class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description="Unique user name")
    full_name: str | None = Field(None, min_length=1, max_length=50, description="Any user name within 50 characters or null")
    email: EmailStr = Field(..., description="Unique user email address")
    phone_number: str | None = Field(None, min_length=10, max_length=15, description="Unique user phone number, can be null")
    avatar_url: str | None = Field(None, min_length=1, max_length=255, description="User avatar url")
    role: UserRoleEnum = Field(UserRoleEnum.USER, description="User role, arguments: user, admin")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=50, description="User password form 8 to 50 characters")


class UserRead(UserBase):
    id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}


class UserUpdate(BaseModel):
    username: str | None= Field(None, min_length=1, max_length=50, description="Unique user name")
    full_name: str | None = Field(None, min_length=1, max_length=50, description="Any user name within 50 characters")
    email: EmailStr | None = Field(None, description="Unique user email address")
    phone_number: str | None = Field(None, min_length=10, max_length=15, description="Unique phone number")
    is_active: bool | None = Field(None, description="Is the user active")


#Project
class ProjectBase(BaseModel):
    owner_id: UUID = Field(..., description="Owner id == User id")
    name: str = Field(..., min_length=1, max_length=100, description="Project name 1-100 characters")
    description: str | None = Field(None, min_length=1, max_length=1000, description="Optional row for project")
    visibility: ProjectVisibilityEnum = Field(ProjectVisibilityEnum.PUBLIC, description="Project visibility arguments: public, private, team")
    

class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100, description="Project name 1-100 characters")
    description: str | None = Field(None, min_length=1, max_length=1000, description="Optional row for project")
    visibility: ProjectVisibilityEnum | None = Field(None, description="Project visibility arguments: public, private, team")


#Board
class BoardBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Board name")
    project_id: UUID = Field(..., description="The project to which the board belongs")
    order: int = Field(0, ge=0, description="Order number, starts with 0")
    background: str = Field("white", min_length=3, max_length=50, description="color code, min_length 3 -> 'red', 4-> #000 ")


class BoardCreate(BoardBase):
    pass


class BoardRead(BoardBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BoardUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=50, description="Board name")
    order: int | None = Field(None, ge=0, description="Order number, starts with 0")
    background: str | None = Field(None, min_length=3, max_length=50, description="color code, min_length 3 -> 'red', 4-> #000 ")


#Column
class ColumnBase(BaseModel):
    board_id: UUID = Field(..., description="The board to which the column belongs")
    name: str = Field(..., min_length=1, max_length=50, description="Column name, 1-50 characters")
    order: int = Field(0, ge=0, description="Order number to display in board by order")
    wip_limit: int | None = Field(None, ge=1, description="The quantity of tasks")
    status: TaskStatusEnum = Field(TaskStatusEnum.TO_DO, description="The status that will be assigned when the task is dragged. arguments: to_do, in_progress, testing, done")

class ColumnCreate(ColumnBase):
    pass


class ColumnRead(ColumnBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ColumnUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=50, description="Column name, 1-50 characters")
    order: int | None = Field(None, ge=0, description="Order number to display in board by order")
    wip_limit: int | None = Field(None, ge=1, description="The quantity of tasks")


#Task
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=50, description="Task title 1-50 characters")
    description: str | None = Field(None, min_length=1, max_length=500, description="Task description 1-500 characters")
    column_id: UUID = Field(..., description="The column to which the task belongs")
    assignee_id: UUID = Field(..., description="The one who is an assigned to the task")
    created_by: UUID = Field(..., description="The one who created the task ")
    priority: TaskPriorityEnum = Field(TaskPriorityEnum.LOW, description="Task priority arguments: low, medium, high, urgent")
    status: TaskStatusEnum = Field(TaskStatusEnum.TO_DO, description="The current status of the task, arguments: to_do, in_progress, testing, done")
    order: int = Field(0, ge=0, description="Order number to display in column by order")
    due_date: datetime = Field(..., description="The date when the task is expected to be completed.")
    completed_at: datetime | None = Field(None, description="The date when the task was completed")


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskUpdate(BaseModel):
    column_id: UUID | None = Field(None, description="The column to which the task belongs")
    assignee_id: UUID | None = Field(None, description="The one who is an assigned to the task")
    title: str | None = Field(None, min_length=1, max_length=50, description="Task title 1-50 characters")
    description: str | None = Field(None, min_length=1, max_length=500, description="Task description 1-500 characters")
    priority: TaskPriorityEnum | None = Field(None, description="Task priority arguments: low, medium, high, urgent")
    status: TaskStatusEnum | None = Field(None, description="The current status of the task, arguments: to_do, in_progress, testing, done")
    order: int | None = Field(None, description="Order number to display in column by order")
    due_date: datetime | None = Field(None, description="The date when the task is expected to be completed.")
    completed_at: datetime | None = Field(None, description="The date when the task was completed")


#TaskAssignemts
class TaskAssignmentBase(BaseModel):
    user_id: UUID
    task_id: UUID


class TaskAssignmentCreate(TaskAssignmentBase):
    pass


class TaskAssignmentRead(TaskAssignmentBase):
    assigned_at: datetime
    
    model_config = {"from_attributes": True}


# Comment
class CommentBase(BaseModel):
    task_id: UUID = Field(..., description="The task to which comment belongs")
    user_id: UUID = Field(..., description="The user who was wrote the comment")
    content: str = Field(..., min_length=1, max_length=2000, description="The comment content")
    parent_id: UUID | None = Field(None, description="The parent(comment) to which this comment belongs, but only if explicity stated")


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CommentUpdate(BaseModel):
    content: str | None = Field(None, min_length=1, max_length=2000, description="The comment content")


class TokenPayload(BaseModel):
    sub: str
    exp: float


class Message(BaseModel):
    data: str
