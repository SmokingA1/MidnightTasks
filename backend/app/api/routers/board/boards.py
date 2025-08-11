from uuid import UUID
from typing import List

from fastapi import APIRouter, HTTPException, status, Path, Query

from app.schemas import BoardCreate, BoardUpdate, BoardRead, Message
from app.api.deps import SessionDep
from app.services.board.board import (
    get_board_by_id,
    get_boards,
    create_board,
    update_board_by_id,
    delete_board_by_id
)

router = APIRouter(prefix="/boards", tags=["Board"])

@router.get("/", response_model=List[BoardRead])
async def read_boards(
    db: SessionDep,
    page: int = Query(1, description="The number of page is required."),
    limit: int = Query(10, description="The number of qty boards is required."),
):
    """
    Receive boards with pagination.
    """

    db_boards = await get_boards(db=db, page=page, limit=limit)

    return db_boards


@router.get("/{board_id}", response_model=BoardRead)
async def read_board_by_id(
    db: SessionDep,
    board_id: UUID,
):
    """
    Receiver board by ID.
    """

    db_board = await get_board_by_id(db=db, board_id=board_id)

    if not db_board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found!")
    
    return db_board


@router.post("/", response_model=BoardRead)
async def create_new_board(
    db: SessionDep, 
    board_create: BoardCreate,
):
    """
    Creating new board.
    """

    new_board = await create_board(db=db, board_create=board_create)

    if not new_board:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while creating new board!"    
        )
    
    return new_board


@router.put("/{board_id}", response_model=BoardRead)
async def update_existing_board(
    db: SessionDep,
    board_id: UUID,
    board_update: BoardUpdate,
):
    """
    Updating existing board by ID.
    """

    db_board = await get_board_by_id(db=db, board_id=board_id)
    
    if not db_board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found!")
    
    updated_board = await update_board_by_id(db=db, board_id=board_id, board_update=board_update)

    if not updated_board:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while updating board"
        )
    
    return updated_board


@router.delete("/", response_model=Message)
async def delete_existing_board(
    db: SessionDep,
    board_id: UUID,
):
    """
    Deleting board by ID.
    """

    db_board = await get_board_by_id(db=db, board_id=board_id)

    if not db_board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    
    deleted_board = await delete_board_by_id(db=db, board_id=board_id)
    
    if not deleted_board:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while deleting board!"
        )
    
    return Message(data="Board deleted succeessfully!")