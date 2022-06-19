from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

import security
from core.db.session import session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


def get_db():
    try:
        db = session()
        yield db
    except:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = security.get_user_from_jwt(token)
    if user_id:
        return user_id
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
