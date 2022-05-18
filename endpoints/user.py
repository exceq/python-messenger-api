from fastapi import APIRouter, Depends, HTTPException
from starlette import status

import security
from crud.user import UserRepository
from deps import get_db, get_current_user
from schemas.user import User, UserModelCreate

router = APIRouter()
user_repository = UserRepository()


@router.get('/', response_model=User)
async def get_user(user_id: int = Depends(get_current_user), db=Depends(get_db)):
    """Получить пользователя по user_id"""
    # raise HTTPException(
    #     status_code=status.HTTP_418_IM_A_TEAPOT,
    #     detail="Incorrect username or password",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    return user_repository.find_by_id(user_id, db=db)


@router.post('/', response_model=User)
async def create_user(user_model_create: UserModelCreate, db=Depends(get_db)):
    """Создать пользователя"""
    hashed_password = security.get_password_hash(user_model_create.password)
    model = user_model_create.dict()
    model.pop('password', None)
    model['hashed_password'] = hashed_password
    return user_repository.create(db=db, **model)


@router.put('/', response_model=User)
async def update_user(user_model_create: UserModelCreate, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    """Изменить пользователя"""
    hashed_password = security.get_password_hash(user_model_create.password)
    user_model_create.password = hashed_password
    return user_repository.update(user_id, db=db, **user_model_create.dict())


@router.delete('/')
async def delete_user(user_id: int = Depends(get_current_user), db=Depends(get_db)):
    """Удалить пользователя"""
    return user_repository.delete(user_id, db=db)
