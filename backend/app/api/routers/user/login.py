from typing import Annotated

from fastapi import HTTPException, status, Response, APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.services.user.user import authenticate, get_user_by_email
from app.schemas import Message
from app.api.deps import SessionDep, CurrentUser
from app.core.security import create_access_token, is_blocked, increment_attempts
from app.core import redis as redis_client

router = APIRouter(tags=['Login'])

@router.post("/login/", response_model=Message)
async def login(
    db: SessionDep,
    response: Response,
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Authenticate user with username and password
    """
    client_ip = request.headers.get("x-forwarded-for", request.client.host)
    print("Ip: ", client_ip)
    key = f"redis_attempts:{client_ip}"
    
    if redis_client.redis is None:
        raise RuntimeError("Please init redis client before trying use connection!")
    
    if await is_blocked(key):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many login attempts. Try again later.")

    db_user = await authenticate(db=db, user_email=form_data.username, user_password=form_data.password)

    if not db_user:
        await increment_attempts(key)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password!")
    
    access_token = create_access_token(sub=db_user.id)
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        secure=False,
        httponly=True,
        samesite='lax'
    )

    return Message(data="Signed in successfully!")