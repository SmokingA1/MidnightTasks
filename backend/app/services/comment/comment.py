from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 

from app.models import Comment
from app.schemas import CommentCreate, CommentUpdate

async def get_comment_by_id(
    *,
    db: AsyncSession,
    comment_id: UUID,
) -> Comment | None:
    db_comment = await db.get(Comment, comment_id)
    return db_comment


async def get_comments(
    *,
    db: AsyncSession,
    page: int = 1,
    limit: int = 20,
) -> List[Comment]:
    query = select(Comment)
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    db_comments = await db.execute(query)
    return db_comments.scalars().all()


async def create_comment(
    *,
    db: AsyncSession,
    comment_create: CommentCreate,
) -> Comment:
    new_comment = Comment(**comment_create.model_dump())
    
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    return new_comment


async def update_comment_by_id(
    *,
    db: AsyncSession,
    comment_id: UUID,
    comment_update: CommentUpdate,
) -> Comment | None:
    db_comment = await get_comment_by_id(db=db, comment_id=comment_id)

    if not db_comment:
        return None
    
    update_data = comment_update.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        if v is not None:
            setattr(db_comment, k, v)

    await db.commit()
    await db.refresh(db_comment)

    return db_comment


async def delete_comment_by_id(
    *,
    db: AsyncSession,
    comment_id: UUID,
) -> Comment | None:
    db_comment = await get_comment_by_id(db=db, comment_id=comment_id)

    if not db_comment:
        return None
    
    await db.delete(db_comment)
    await db.commit()

    return db_comment