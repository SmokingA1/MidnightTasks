from typing import Annotated
from datetime import datetime, timezone, timedelta

from jwt import DecodeError, InvalidTokenError
import jwt
from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError

from app.core.database import get_db
from app.core.config import settings
from app.models import User
from app.schemas import TokenPayload

SessionDep = Annotated[AsyncSession, Depends(get_db)]

async def get_current_user(request: Request, db: SessionDep) -> User:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing!")

    try:
        token_payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**token_payload)

        if datetime.now(timezone.utc).timestamp() > token_data.exp:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        
    except (ValidationError, InvalidTokenError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token, error decoding!")

    db_user = await db.get(User, str(token_data.sub))

    if not db_user:
        HTTPException(status.HTTP_404_NOT_FOUND, "User not found!")
    
    return db_user

CurrentUser = Annotated[User, Depends(get_current_user)]