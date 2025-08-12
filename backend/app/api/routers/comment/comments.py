from uuid import UUID
from typing import List

from fastapi import APIRouter, HTTPException, status, Query

from app.schemas import CommentCreate, CommentUpdate, CommentRead, Message
from app.api.deps import SessionDep
from app.services.comment.comment import (
    get_comment_by_id,
    get_comments,
    create_comment,
    update_comment_by_id,
    delete_comment_by_id,
)

router = APIRouter(prefix="/comments", tags=["Comment"])

@router.get("/", response_model=List[CommentRead])
async def read_comments(
    db: SessionDep,
    page: int = Query(1, description="The number of page is required."),
    limit: int = Query(20, description="The number of qty comments is required."),
):
    """
    Receive comments with pagination.
    """

    db_comments = await get_comments(db=db, page=page, limit=limit)

    return db_comments


@router.get("/{comment_id}", response_model=CommentRead)
async def read_comment_by_id(
    db: SessionDep,
    comment_id: UUID,
):
    """
    Receive comment by ID.
    """

    db_comment = await get_comment_by_id(db=db, comment_id=comment_id)

    if not db_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found!")
    
    return db_comment


@router.post("/", response_model=CommentRead)
async def create_new_comment(
    db: SessionDep,
    comment_create: CommentCreate,
):
    """
    Creating new comment.
    """

    new_comment = await create_comment(db=db, comment_create=comment_create)

    if not new_comment:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while creating new comment!"
        )
    
    return new_comment


@router.put("/{comment_id}", response_model=CommentRead)
async def update_existing_comment(
    db: SessionDep,
    comment_id: UUID,
    comment_update: CommentUpdate,
):
    """
    Update existing comment by ID.
    """

    db_comment = await get_comment_by_id(db=db, comment_id=comment_id)

    if not db_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found!")
    
    updated_comment = await update_comment_by_id(db=db, comment_id=comment_id, comment_update=comment_update)

    if not updated_comment:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while updating comment!"
        )
    
    return updated_comment


@router.delete("/{comment_id}", response_model=Message)
async def delete_existing_comment(
    db: SessionDep,
    comment_id: UUID,
):
    """
    Deleting comment by ID.
    """

    db_comment = await get_comment_by_id(db=db, comment_id=comment_id)

    if not db_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found!")
    
    deleted_comment = await delete_comment_by_id(db=db, comment_id=comment_id)

    if not deleted_comment:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while deleting comment!"
        )
    
    return Message(data="Comment deleted successfully!")