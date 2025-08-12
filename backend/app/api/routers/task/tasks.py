from uuid import UUID
from typing import List

from fastapi import APIRouter, HTTPException, status, Query

from app.schemas import TaskCreate, TaskRead, TaskUpdate, Message
from app.api.deps import SessionDep
from app.services.task.task import (
    get_task_by_id,
    get_tasks,
    create_task,
    update_task_by_id,
    delete_task_by_id,
)

router = APIRouter(prefix="/tasks", tags=["Task"])

@router.get("/", response_model=List[TaskRead])
async def read_tasks(
    db: SessionDep,
    page: int = Query(1, description="The number of page is required."),
    limit: int = Query(20, description="The number of qty column is required."),
):
    """
    Receive list of tasks with pagination.
    """

    db_tasks = await get_tasks(db=db, page=page, limit=limit)

    return db_tasks


@router.get("/{task_id}", response_model=TaskRead)
async def read_task_by_id(
    db: SessionDep,
    task_id: UUID,
):
    """
    Receive task by ID.
    """

    db_task = await get_task_by_id(db=db, task_id=task_id)

    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return db_task


@router.post("/", response_model=TaskRead)
async def create_new_task(
    db: SessionDep,
    task_create: TaskCreate,
):
    """
    Creating new task.
    """

    new_task = await create_task(db=db, task_create=task_create)

    if not new_task:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while creating new task."    
        )
    
    return new_task


@router.put("/{task_id}", response_model=TaskRead)
async def update_existing_task(
    db: SessionDep,
    task_update: TaskUpdate,
    task_id: UUID,
):
    """
    Updating existing task by ID.
    """

    db_task = await get_task_by_id(db=db, task_id=task_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found!"
        )
    
    updated_task = await update_task_by_id(
        db=db, task_id=task_id, task_update=task_update
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while updating task."
        )
    
    return updated_task


@router.delete("/{task_id}", response_model=Message)
async def delete_existing_task(
    db: SessionDep,
    task_id: UUID,
):
    """
    Deleting existing task by ID.
    """

    db_task = await get_task_by_id(db=db, task_id=task_id)

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found!"
        )
    
    deleted_task = await delete_task_by_id(db=db, task_id=task_id)

    if not deleted_task:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while deleting task."
        )
    
    return Message(data="Task deleted successfully!")