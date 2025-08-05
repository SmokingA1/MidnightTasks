from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, Enum, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.core.database import Base, TimestampMixin, TZDateTime
from app.enums import TaskStatusEnum, TaskPriorityEnum, ProjectVisibilityEnum

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(15), nullable=True, unique=True, index=True)
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    projects: Mapped[list["Project"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    created_tasks: Mapped[list["Task"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    tasks_assignee: Mapped[list["Task"]] = relationship(back_populates="assignee", passive_deletes=True)
    
    tasks: Mapped[list["TaskAssignment"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.username}', email='{self.email}')>"


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", name="fk_projects_users_id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    visibility: Mapped[ProjectVisibilityEnum] = mapped_column(Enum(ProjectVisibilityEnum, name="projectvisibility"), default=ProjectVisibilityEnum.PUBLIC, nullable=False)

    boards: Mapped[list["Board"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    user: Mapped["User"] = relationship(back_populates="projects")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"


class Board(Base, TimestampMixin):
    __tablename__ = "boards"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE", name="fk_boards_projects_id"), nullable=False, index=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    background: Mapped[str] = mapped_column(String(50), default="white")
    
    columns: Mapped[list["Column"]] = relationship(back_populates="board", cascade="all, delete-orphan")
    project: Mapped["Project"] = relationship(back_populates="boards")

    def __repr__(self):
        return f"<Board(id={self.id}, name='{self.name}')>"


class Column(Base, TimestampMixin):
    __tablename__ = "columns"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    board_id: Mapped[UUID] = mapped_column(ForeignKey("boards.id", ondelete="CASCADE", name="fk_columns_boards_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    wip_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)

    tasks: Mapped[list["Task"]] = relationship(back_populates="column", cascade="all, delete-orphan")
    board: Mapped["Board"] = relationship(back_populates="columns")

    def __repr__(self):
        return f"<Column(id={self.id}, name='{self.name}')>"


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    column_id: Mapped[UUID] = mapped_column(ForeignKey("columns.id", ondelete="CASCADE", name="fk_tasks_columns_id"), nullable=False)
    assignee_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)    
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", name="fk_tasks_users_id"), nullable=False)
    priority: Mapped[TaskPriorityEnum] = mapped_column(Enum(TaskPriorityEnum, name="priority"), nullable=False, default=TaskPriorityEnum.LOW)
    status: Mapped[TaskStatusEnum] = mapped_column(Enum(TaskStatusEnum, name="taskstatus"), nullable=False, default=TaskStatusEnum.OPEN)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    due_date: Mapped[datetime] = mapped_column(TZDateTime(), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(TZDateTime(), nullable=True)

    comments: Mapped[list["Comment"]] = relationship(back_populates="task", cascade="all, delete-orphan")

    assignee: Mapped["User" | None] = relationship(back_populates="tasks_assignee")
    column: Mapped["Column"] = relationship(back_populates="tasks")
    user: Mapped["User"] = relationship(back_populates="created_tasks")

    assignments: Mapped[list["TaskAssignment"]] = relationship(back_populates="task", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', priority='{self.priority}')>"


class TaskAssignment(Base): # task <task_assignments> user; 1 task -> many users, 1 user -> many tasks
    __tablename__ = "task_assignments"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", name="fk_task_assignments_users_id"), nullable=False, index=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE", name="fk_task_assignments_tasks_id"), nullable=False, index=True)
    assigned_at: Mapped[datetime] = mapped_column(TZDateTime(), default=datetime.now(timezone.utc))

    task: Mapped["Task"] = relationship(back_populates="assignments")
    user: Mapped["User"] = relationship(back_populates="tasks")

    __table_args__ = (
        PrimaryKeyConstraint("task_id", "user_id"),
    )

    def __repr__(self):
        return f"<TaskAssignment(user_id={self.user_id}, task_id={self.task_id})>"


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE", name="fk_comments_tasks_id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", name="fk_comments_users_id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    parent_id: Mapped[UUID | None] = mapped_column(ForeignKey("comments.id", name="fk_comments_comments_id"), nullable=True)

    task: Mapped["Task"] = relationship(back_populates="comments")
    children: Mapped[list["Comment"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    parent: Mapped["Comment" | None] = relationship(
        back_populates="children",
        remote_side=[id],
        uselist=False
    )

    def __repr__(self):
        return f"<Comment(id={self.id}, content='{self.content}')>"
    

# class Attachment(Base, TimestampMixin):
#     pass