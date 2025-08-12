from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate

async def get_task_by_id(
    *,
    db: AsyncSession,
    task_id: UUID,
) -> Task | None:
    db_task = await db.get(Task, task_id)
    return db_task


async def get_tasks(
    *,
    db: AsyncSession,
    page: int = 1,
    limit: int = 20,
) -> List[Task]:
    query = select(Task)
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    db_tasks = await db.execute(query)
    return db_tasks.scalars().all()


async def create_task(
    *,
    db: AsyncSession,
    task_create: TaskCreate,
) -> Task:
    new_task = Task(**task_create.model_dump())

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return new_task


async def update_task_by_id(
    *,
    db: AsyncSession,
    task_id: UUID,
    task_update: TaskUpdate,
) -> Task | None:
    db_task = await get_task_by_id(db=db, task_id=task_id)
    
    if not db_task:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        if v is not None:
            setattr(db_task, k, v)
        elif k in ("description"):
            setattr(db_task, k, v)

    await db.commit()
    await db.refresh(db_task)

    return db_task


async def delete_task_by_id(
    *,
    db: AsyncSession,
    task_id: UUID,
) -> Task | None:
    db_task = await get_task_by_id(db=db, task_id=task_id)
    
    if not db_task:
        return None
    
    await db.delete(db_task)
    await db.commit()

    return db_task