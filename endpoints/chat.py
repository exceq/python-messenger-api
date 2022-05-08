from fastapi import APIRouter, Depends, HTTPException
from starlette import status

import crud.chat as chat_repository
import crud.user as user_repository
from schemas.chat import Chat, ChatModel
from deps import get_db

router = APIRouter()


@router.get('/{chat_id}', response_model=Chat)
async def get_chat(chat_id: int, db=Depends(get_db)):
    """Получить чат по chat_id"""
    chat = chat_repository.find_by_id(chat_id, db=db)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found chat with id {chat_id}")
    return chat


@router.post('/', response_model=Chat)
async def create_chat(chat: ChatModel, db=Depends(get_db)):
    """Создать чат"""
    return chat_repository.create(chat_model=chat, db=db)


@router.put('/{chat_id}', response_model=Chat)
async def update_chat(chat_id: int, chat_model: ChatModel, db=Depends(get_db)):
    """Изменить чат"""
    return chat_repository.update(chat_id, chat_model, db=db)


@router.delete('/{chat_id}')
async def delete_chat(chat_id: int, db=Depends(get_db)):
    """Удалить чат"""
    return chat_repository.delete(chat_id, db=db)


@router.put('/{chat_id}/add_user')
async def add_user_to_chat(chat_id: int, user_id: int, db=Depends(get_db)):
    """Добавить пользователя в чат"""
    chat = chat_repository.add_user_to_chat(chat_id=chat_id, user_id=user_id, db=db)
    return chat
