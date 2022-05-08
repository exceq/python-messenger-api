from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from crud.message import MessageRepository
from deps import get_db
from schemas.message import Message, MessageModel

router = APIRouter()
message_repository = MessageRepository()


@router.get('/{message_id}', response_model=Message)
async def get_message(message_id: int, db=Depends(get_db)):
    """Получить сообщение по message_id"""
    message = message_repository.find_by_id(message_id, db=db)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found message with id {message_id}")
    return message


@router.post('/', response_model=Message)
async def create_message(message_model: MessageModel, db=Depends(get_db)):
    """Создать сообщение по message_id"""
    message = message_repository.create(db=db, **message_model.dict())
    return message


@router.put('/{message_id}', response_model=Message)
async def edit_message(message_id: int, text: str, db=Depends(get_db)):
    """Изменить сообщение по message_id"""
    message = message_repository.update(id=message_id, db=db, text=text)
    return message


@router.delete('/{message_id}')
async def delete_message(message_id: int, db=Depends(get_db)):
    """Удалить сообщение по message_id"""
    message = message_repository.delete(id=message_id, db=db)
    return message


@router.get('/{chat_id}/last_messages', response_model=List[Message])
async def get_last_messages(chat_id: int, db=Depends(get_db), offset: int = 0, limit: int = 20):
    """Получить сообщения чата начиная с offset """
    messages = message_repository.get_last_messages(chat_id=chat_id, db=db, offset=offset, limit=limit)
    return messages
