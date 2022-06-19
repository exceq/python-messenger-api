import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from crud.chat import ChatRepository
from crud.message import MessageRepository
from deps import get_db
from schemas.chat import ChatModel, Chat

from deps import get_current_user
from schemas.message import Message

router = APIRouter()
chat_repository = ChatRepository()
message_repository = MessageRepository()


@router.get('/{chat_id}', response_model=Chat)
async def get_chat(chat_id: int, db=Depends(get_db)):
    """Получить чат по chat_id"""
    chat = chat_repository.find_by_id(id=chat_id, db=db)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found chat with id {chat_id}")
    return chat


@router.post('/', response_model=Chat)
async def create_chat(chat_model: ChatModel, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    """Создать чат"""
    return chat_repository.create_chat(db=db, chat_model=chat_model, creator_user_id=user_id)


@router.put('/{chat_id}', response_model=Chat)
async def update_chat(chat_id: int, chat_model: ChatModel, user_id: int = Depends(get_current_user),
                      db=Depends(get_db)):
    """Изменить чат"""
    chat = chat_repository.find_by_id(chat_id, db=db)
    if int(chat.creator_user_id) != int(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Can't update chat with other owner")
    return chat_repository.update(id=chat_id, db=db, **chat_model.dict())


@router.delete('/{chat_id}')
async def delete_chat(chat_id: int, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    """Удалить чат"""
    chat = chat_repository.find_by_id(chat_id, db=db)
    if int(chat.creator_user_id) != int(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Can't delete chat with other owner")
    return chat_repository.delete(chat_id, db=db)


@router.put('/{chat_id}/add_user')
async def add_user_to_chat(chat_id: int, new_user_id: int, user_id: int = Depends(get_current_user),
                           db=Depends(get_db)):
    """Добавить пользователя в чат"""
    chat = chat_repository.add_user_to_chat(chat_id=chat_id, user_id=new_user_id, db=db)
    return chat


@router.get('/{chat_id}/last_messages', response_model=List[Message])
async def get_last_messages(chat_id: int, user_id: int = Depends(get_current_user), db=Depends(get_db), offset: int = 0,
                            limit: int = 20):
    """
    Возвращает последние N сообщений из чата равное limit начиная с offser,
    """
    return message_repository.get_last_messages(chat_id=chat_id, db=db, offset=offset, limit=limit)


@router.get('/{chat_id}/last_active')
async def get_last_active_chats(user_id: int = Depends(get_current_user), db=Depends(get_db)):
    """
    Возвращает последние N сообщений из чата равное limit начиная с offser,
    """
    return chat_repository.get_last_active_chats(user_id=user_id, db=db)
