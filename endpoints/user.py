from fastapi import APIRouter, Depends, HTTPException
from starlette import status

import crud.user as user_repository
from schemas.user import User, UserModel
from deps import get_db

router = APIRouter()


@router.get('/{user_id}', response_model=User)
async def get_user(user_id: int, db=Depends(get_db)):
    """Получить пользователя по user_id"""
    user = user_repository.find_by_id(user_id, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found user with id {user_id}")
    return user


@router.post('/', response_model=User)
async def create_user(user: UserModel, db=Depends(get_db)):
    """Создать пользователя"""
    return user_repository.create(user_model=user, db=db)


@router.put('/{user_id}', response_model=User)
async def update_user(user_id: int, user_model: UserModel, db=Depends(get_db)):
    """Изменить пользователя"""
    return user_repository.update(user_id, user_model, db=db)


@router.delete('/{user_id}')
async def delete_user(user_id: int, db=Depends(get_db)):
    """Удалить пользователя"""
    return user_repository.delete(user_id, db=db)
