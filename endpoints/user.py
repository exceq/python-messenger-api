from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from crud.user import UserRepository
from schemas.user import User, UserModel
from deps import get_db

router = APIRouter()
user_repository = UserRepository()


@router.get('/{user_id}', response_model=User)
async def get_user(user_id: int, db=Depends(get_db)):
    """Получить пользователя по user_id"""
    user = user_repository.find_by_id(id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found user with id {user_id}")
    return user


@router.post('/', response_model=User)
async def create_user(user: UserModel, db=Depends(get_db)):
    """Создать пользователя"""
    return user_repository.create(db=db, **user.dict())


@router.put('/{user_id}', response_model=User)
async def update_user(user_id: int, user_model: UserModel, db=Depends(get_db)):
    """Изменить пользователя"""
    return user_repository.update(user_id, db=db, **user_model.dict())


@router.delete('/{user_id}')
async def delete_user(user_id: int, db=Depends(get_db)):
    """Удалить пользователя"""
    return user_repository.delete(user_id, db=db)
