from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Column
from app.schemas import ColumnCreate, ColumnUpdate

async def get_column_by_id(
    *,
    db: AsyncSession,
    column_id: UUID,
) -> Column | None:
    db_column = await db.get(Column, column_id)
    return db_column


async def get_columns(
    *,
    db: AsyncSession,
    page: int = 1,
    limit: int = 20,
) -> List[Column]:
    query = select(Column)
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    db_columns = await db.execute(query)
    return db_columns.scalars().all()


async def create_column(
    *,
    db: AsyncSession,
    column_create: ColumnCreate,
) -> Column:
    new_column = Column(**column_create.model_dump())

    db.add(new_column)
    await db.commit()
    await db.refresh(new_column)

    return new_column


async def update_column(
    *,
    db: AsyncSession,
    column_id: UUID,
    column_update: ColumnUpdate,
) -> Column | None:
    db_column = await get_column_by_id(db=db, column_id=column_id)

    if not db_column:
        return None
    
    update_data = column_update.model_dump()
    for k, v in update_data.items():
        if v is not None:
            setattr(db_column, k, v)
        elif k in ("wip_limit"):
            setattr(db_column, k, v)

    await db.commit()
    await db.refresh(db_column)
    
    return db_column


async def delete_column_by_id(
    *,
    db: AsyncSession,
    column_id: UUID,
) -> Column | None:
    db_column = await get_column_by_id(db=db, column_id=column_id)

    if not db_column:
        return None
    
    await db.delete(db_column)
    await db.commit()

    return db_column