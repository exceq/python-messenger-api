from fastapi import APIRouter

import crud.user as user_repository
from schemas.user import User, UserModel

router = APIRouter()


@router.get('/{user_id}', response_model=User)
async def get_user(user_id: int):
    """Получить пользователя по user_id"""

    return user_repository.get(user_id)


@router.post('/', response_model=User)
async def create_user(user: UserModel):
    """Создать пользователя"""
    return user_repository.create(user)


@router.put('/{user_id}', response_model=User)
async def update_user(user_id: int, user: UserModel):
    """Изменить пользователя"""
    return user_repository.update(user_id, user)


@router.delete('/{user_id}')
async def update_user(user_id: int):
    """Удалить пользователя"""
    return user_repository.delete(user_id)
