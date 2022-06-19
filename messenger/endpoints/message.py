import datetime
from os import getenv

import pytz
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.broker.celery import celery_app
from crud.message import MessageRepository
from deps import get_current_user, get_db
from schemas.message import Message, MessageModel, MessageModelAsync

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
async def create_message(message_model: MessageModel, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    """Создать сообщение"""
    model = message_model.__dict__
    model['user_id'] = user_id
    return message_repository.create(db=db, **model)


@router.put('/{message_id}', response_model=Message)
async def edit_message(message_id: int, text: str, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    """Изменить сообщение по message_id"""
    message = message_repository.find_by_id(message_id, db=db)
    if int(message.user_id) != int(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Can't edit not your message. {message_id}")
    return message_repository.update(id=message_id, db=db, text=text)


@router.delete('/{message_id}')
async def delete_message(message_id: int, user_id: int = Depends(get_current_user), db=Depends(get_db)):
    """Удалить сообщение по message_id"""
    return message_repository.delete(id=message_id, db=db)


@router.post('/async')
async def create_message_async(model: MessageModelAsync, user_id: int = Depends(get_current_user)):
    """Отправить сообщение с задержкой в N секунд"""
    model.user_id = user_id
    send_time = datetime.datetime.now() + datetime.timedelta(seconds=model.delay_in_seconds)
    timezone = pytz.timezone(getenv("TZ"))
    dt_with_timezone = timezone.localize(send_time)
    celery_app.send_task('queue.send_async', eta=dt_with_timezone, kwargs=model.__dict__)
    return 1
