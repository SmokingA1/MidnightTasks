from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import TaskAssignment
from app.schemas import TaskAssignmentCreate

async def get_task_assignment_by_id(
    *,
    db: AsyncSession,
    user_id: UUID,
    task_id: UUID
) -> TaskAssignment | None:
    query = select(TaskAssignment).where(TaskAssignment.user_id == user_id, TaskAssignment.task_id == task_id)
    db_ta = await db.execute(query)
    return db_ta.scalars().first()


async def get_task_assignments(
    *,
    db: AsyncSession,
    page: int = 1,
    limit: int = 20,
) -> List[TaskAssignment]:
    query = select(TaskAssignment)
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    db_tas = await db.execute(query)
    return db_tas.scalars().all()


async def create_task_assignment(
    *,
    db: AsyncSession,
    task_assignment_create: TaskAssignmentCreate,
) -> TaskAssignment:
    new_ta = TaskAssignment(**task_assignment_create.model_dump())
    
    db.add(new_ta)
    await db.commit()
    await db.refresh(new_ta)

    return new_ta


async def delete_task_assignment_by_id(
    *,
    db: AsyncSession,
    user_id: UUID,
    task_id: UUID,
) -> TaskAssignment | None:
    db_ta = await get_task_assignment_by_id(db=db, user_id=user_id, task_id=task_id)

    if not db_ta:
        return None
    
    await db.delete(db_ta)
    await db.commit()

    return db_ta
    