from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Board
from app.schemas import BoardCreate, BoardUpdate

async def get_board_by_id(
    *,
    db: AsyncSession,
    board_id: UUID,
) -> Board | None:
    db_board = await db.get(Board, board_id)
    return db_board


async def get_boards(
    *,
    db: AsyncSession,
    page: int = 1,
    limit: int = 20,
) -> List[Board]:
    query = select(Board)
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    db_boards = await db.execute(query)
    return db_boards.scalars().all()


async def create_board(
    *,
    db: AsyncSession,
    board_create: BoardCreate,
) -> Board:
    new_board = Board(**board_create.model_dump())

    db.add(new_board)
    await db.commit()
    await db.refresh(new_board)

    return new_board


async def update_board_by_id(
    *,
    db: AsyncSession,
    board_id: UUID,
    board_update: BoardUpdate,
) -> Board | None:
    db_board = await get_board_by_id(db=db, board_id=board_id)

    if not db_board:
        return None
    
    update_data = board_update.model_dump(exclude_unset=True)
    for k,v in update_data.items():
        if v is not None:
            setattr(db_board, k, v)

    await db.commit()
    await db.refresh(db_board)

    return db_board


async def delete_board_by_id(
    *,
    db: AsyncSession,
    board_id: UUID,
) -> Board | None:
    db_board = await get_board_by_id(db=db, board_id=board_id)
    
    if not db_board:
        return None
    
    await db.delete(db_board)
    await db.commit()

    return db_board