from uuid import UUID
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Project
from app.schemas import ProjectCreate, ProjectUpdate

async def get_project_by_id(
    *,
    db: AsyncSession,
    project_id: UUID,
) -> Project | None:
    db_project = await db.get(Project, project_id)
    return db_project


async def get_projects(
    *,
    db: AsyncSession,
    page: int = 1,
    limit: int = 20,
) -> List[Project]:
    query = select(Project)
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    db_projects = await db.execute(query)
    return db_projects.scalars().all()


async def create_project(
    *,
    db: AsyncSession,
    project_create: ProjectCreate,
) -> Project:
    new_project = Project(**project_create.model_dump())

    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)

    return new_project


async def update_project_by_id(
    *,
    db: AsyncSession,
    project_id: UUID,
    project_update: ProjectUpdate,
) -> Project | None:
    db_project = await get_project_by_id(db=db, project_id=project_id)
    
    if not db_project:
        return None
    
    update_data = project_update.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        if v is not None:
            setattr(db_project, k, v) # if v is not None, any value except None, we set by k value, but if None go down
        elif k in ("description"):
            setattr(db_project, k, v) # if v is None but k is "description" what is okay for model, we can description set as null its okay
     
    await db.commit()
    await db.refresh(db_project)

    return db_project


async def delete_project_by_id(
    *,
    db: AsyncSession,
    project_id: UUID,
) -> Project | None:
    db_project = await get_project_by_id(db=db, project_id=project_id)

    if not db_project:
        return None
    
    await db.delete(db_project)
    await db.commit()

    return db_project