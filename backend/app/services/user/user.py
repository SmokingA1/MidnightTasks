from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas import UserCreate, UserUpdate
from app.models import User
from app.core.security import hash_password, verify_password

async def get_user_by_id(*, db: AsyncSession, user_id: UUID) -> User | None: 
    db_user = await db.get(User, user_id)
    return db_user


async def get_users(
    *,
    db: AsyncSession,
    page: int = 1,
    limit: int = 20,
) -> List[User]:
    query = select(User)
    offset = (page - 1 ) * limit
    query = query.offset(offset).limit(limit)

    db_users = await db.execute(query)
    return db_users.scalars().all()


async def get_user_by_email(
    *,
    db: AsyncSession,
    user_email: str
) -> User | None:
    query = select(User).where(User.email == user_email)
    db_user = await db.execute(query)

    return db_user.scalars().first()


async def get_user_by_phone_number(
    *,
    db: AsyncSession,
    user_phone_number: str
) -> User | None:
    query = select(User).where(User.phone_number == user_phone_number)
    db_user = await db.execute(query)

    return db_user.scalars().first()


async def get_user_by_username(
    *,
    db: AsyncSession,
    username: str,
) -> User | None:
    query = select(User).where(User.username == username)
    db_user = await db.execute(query)

    return db_user.scalars().first()


async def create_user(
    *,
    db: AsyncSession,
    user_create: UserCreate,
) -> User:
    new_user = User(
        username=user_create.username,
        full_name=user_create.full_name,
        hashed_password=hash_password(user_create.password),
        email=user_create.email,
        phone_number=user_create.phone_number,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def update_user_by_id(
    *,
    db: AsyncSession,
    user_id: UUID,  
    user_update: UserUpdate,
) -> User | None:
    db_user = await get_user_by_id(db=db, user_id=user_id)
    
    if not db_user: 
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        if v is not None:
            setattr(db_user, k, v)
        elif k in ("full_name", "phone_number"):
            setattr(db_user, k, v)

    await db.commit()
    await db.refresh(db_user)

    return db_user


async def delete_user_by_id(
    *,
    db: AsyncSession,
    user_id: UUID,
) -> User | None:
    db_user = await get_user_by_id(db=db, user_id=user_id)
    
    if not db_user:
        return None
    
    await db.delete(db_user)
    await db.commit()

    return db_user


async def authenticate(
    *, 
    db: AsyncSession, 
    user_email: str,
    user_password: str
) -> User | None:
    db_user = await get_user_by_email(db=db, user_email=user_email)

    if not db_user or not verify_password(plain_password=user_password, hashed_password=db_user.hashed_password):
        return None
    
    return db_user