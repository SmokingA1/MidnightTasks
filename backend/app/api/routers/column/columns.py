from uuid import UUID
from typing import List

from fastapi import APIRouter, HTTPException, status, Query

from app.schemas import ColumnCreate, ColumnRead, ColumnUpdate, Message
from app.api.deps import SessionDep
from app.services.column.column import (
    get_column_by_id,
    get_columns,
    create_column,
    update_column,
    delete_column_by_id,
)

router = APIRouter(prefix="/columns", tags=["Column"])

@router.get("/", response_model=List[ColumnRead])
async def read_columns(
    db: SessionDep,
    page: int = Query(1, description="The number of page is required."),
    limit: int = Query(20, description="The number of qty column is required."),
):
    """
    Receive columns with pagination
    """

    db_columns = await get_columns(db=db, page=page, limit=limit)

    return db_columns


@router.get("/{columnd_id}", response_model=ColumnRead)
async def read_column_by_id(
    db: SessionDep,
    column_id: UUID,
):
    """
    Receive column by ID.
    """

    db_column = await get_column_by_id(db=db, column_id=column_id)

    if not db_column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found!")
    
    return db_column


@router.post("/", response_model=ColumnRead)
async def create_new_column(
    db: SessionDep,
    column_create: ColumnCreate,
):
    """
    Creating new column.
    """

    new_column = await create_column(db=db, column_create=column_create)

    if not new_column:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while creating new column."
        )
    
    return new_column


@router.put("/{column_id}", response_model=ColumnRead)
async def update_existing_column(
    db: SessionDep,
    column_id: UUID,
    column_update: ColumnUpdate,
):
    """
    Update existing column by ID.
    """

    db_column = await get_column_by_id(db=db, column_id=column_id)

    if not db_column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found!")
    
    updated_column = await update_column(db=db, column_id=column_id, column_update=column_update)

    if not updated_column:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while udpating column."
        )
    
    return updated_column


@router.delete("/{column_id}", response_model=Message)
async def delete_existing_column(
    db: SessionDep,
    column_id: UUID,
):
    """
    Deleting existing column by ID.
    """

    db_column = await get_column_by_id(db=db, column_id=column_id)

    if not db_column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found!")
    
    deleted_column = await delete_column_by_id(db=db, column_id=column_id)

    if not deleted_column:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while deleting column."
        )
    
    return Message(data="Column deleted successfully!")