from uuid import UUID
from typing import List

from fastapi import APIRouter, status, HTTPException, Path, Query

from app.schemas import UserCreate, UserRead, UserUpdate, Message
from app.services.user.user import (
    get_user_by_email,
    get_user_by_id,
    get_user_by_phone_number,
    get_user_by_username,
    get_users,
    create_user,
    update_user_by_id,
    delete_user_by_id
) 
from app.api.deps import SessionDep, CurrentUser

router = APIRouter(prefix="/users", tags=['User'])


@router.get("/", response_model=List[UserRead])
async def read_users(
    db: SessionDep,
    page: int = Query(1, description="The number of page is required."),
    limit: int = Query(20, description="The number of qty users is required."),
):
    """
    Receiver user with pagination.
    """
    
    db_users = await get_users(db=db, page=page, limit=limit)

    return db_users


@router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: CurrentUser
):
    """
    Receive user by jwt from cookie.
    """

    return current_user


@router.get("/{user_id}", response_model=UserRead)
async def read_user_by_id(
    db: SessionDep,
    current_user: CurrentUser,
    user_id: UUID = Path(..., description="User id is required."),
):
    """
    Receive user by id.
    """

    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Rights denied!")

    db_user = await get_user_by_id(db=db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    
    return db_user


@router.get("/email/{user_email}", response_model=UserRead)
async def read_user_by_email(
    db: SessionDep,
    user_email: str = Path(..., description="User email is required."),
):
    """
    Receive user by email.
    """

    db_user = await get_user_by_email(db=db, user_email=user_email)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    
    return db_user


@router.get("/phone-number/{user_phone_number}", response_model=UserRead)
async def read_user_by_phone_number(
    db: SessionDep,
    user_phone_number: str = Path(..., description="User phone number is required."),
):
    """
    Receiver user by phone number.
    """

    db_user = await get_user_by_phone_number(db=db, user_phone_number=user_phone_number)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    
    return db_user


@router.post("/", response_model=UserRead)
async def create_new_user(
    db: SessionDep,
    user_create: UserCreate,
):
    """
    Creating new user.
    """

    existing_email = await get_user_by_email(db=db, user_email=user_create.email)
    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Such email already exists!")
    
    if user_create.phone_number is not None:
        existing_phone = await get_user_by_phone_number(db=db, user_phone_number=user_create.phone_number)
        if existing_phone:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Such phone number already exists!")

    existing_username = await get_user_by_username(db=db, username=user_create.username)
    if existing_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Such username already exists!")

    created_user = await create_user(db=db, user_create=user_create)

    return created_user


@router.put("/{user_id}", response_model=UserRead)
async def update_existing_user(
    db: SessionDep,
    user_update: UserUpdate,
    current_user: CurrentUser,
    user_id: UUID = Path(..., description="User ID is required!"),
):
    """
    Update user by id.
    """
    
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Rights denied!")

    db_user = await get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if user_update.username:
        existing_username_user = await get_user_by_username(db=db, username=user_update.username)
        if existing_username_user and existing_username_user.id != db_user.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Such username already exists")

    if user_update.email:
        existing_email_user = await get_user_by_email(db=db, user_email=user_update.email)
        if existing_email_user and existing_email_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Such email already exists!"
            )
    
    if user_update.phone_number:
        existing_phone_user = await get_user_by_phone_number(db=db, user_phone_number=user_update.phone_number)
        if existing_phone_user and existing_phone_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Such phone number already exists!"
            )
    updated_user = await update_user_by_id(db=db, user_update=user_update, user_id=user_id)
    return updated_user


@router.delete("/{user_id}", response_model=Message)
async def delete_existing_user(
    db: SessionDep,
    current_user: CurrentUser,
    user_id: UUID = Path(..., description="User ID is required!"),
):
    """
    Deleting user by id
    """

    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Rights denied!")

    deleted_user = await delete_user_by_id(db=db, user_id=user_id)

    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    
    return Message(data="User was deleted successfully!")