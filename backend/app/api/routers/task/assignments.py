from uuid import UUID
from typing import List

from fastapi import APIRouter, HTTPException, status, Query

from app.api.deps import SessionDep
from app.schemas import TaskAssignmentCreate, TaskAssignmentRead, Message
from app.services.task.assignment import (
    get_task_assignment_by_id,
    get_task_assignments,
    create_task_assignment,
    delete_task_assignment_by_id,
)

router = APIRouter(prefix="/task-assignments", tags=["TaskAssignment"])

@router.get("/", response_model=List[TaskAssignmentRead])
async def read_task_assginemts(
    db: SessionDep,
    page: int = Query(1, description="The number of page is required."),
    limit: int = Query(20, description="The number of qty column is required."),
):
    """
    Receive task assignments with pagination.
    """

    db_task_assignments = await get_task_assignments(db=db, page=page, limit=limit)

    return db_task_assignments


@router.get("/task/{task_id}/user/{user_id}", response_model=TaskAssignmentRead)
async def read_task_assignment_by_id(
    db: SessionDep,
    task_id: UUID,
    user_id: UUID,
):
    """
    Receive task assignment by user and task ID.
    """

    db_task_assignment = await get_task_assignment_by_id(db=db, user_id=user_id, task_id=task_id)

    if not db_task_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task assignment not found!"
        )

    return db_task_assignment


@router.post("/", response_model=TaskAssignmentRead)
async def create_new_task_assignment(
    db: SessionDep,
    task_assignment_create: TaskAssignmentCreate,
):
    """
    Create new task assignment.
    """

    new_task_assignment = await create_task_assignment(db=db, task_assignment_create=task_assignment_create)

    if not new_task_assignment:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,            
            detail="Something went wrong while creating new task assignment!"
        )
    
    return new_task_assignment 


@router.delete("/task/{task_id}/user/{user_id}", response_model=Message)
async def delete_existing_task_assignment(
    db: SessionDep,
    user_id: UUID,
    task_id: UUID
):
    """
    Deleting existing task assignment by user and task ID.
    """

    db_task_assignment = await get_task_assignment_by_id(db=db, user_id=user_id, task_id=task_id)

    if not db_task_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task assignment not found!"
        )
    
    deleted_task_assignment = await delete_task_assignment_by_id(db=db, user_id=user_id, task_id=task_id)

    if not deleted_task_assignment:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while deleting task assignment!"
        )
    
    return Message(data="Task assignment deleted successfully!")