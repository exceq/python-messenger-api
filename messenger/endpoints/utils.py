"""Различные методы проверки функционала"""
import json
import logging

from fastapi import APIRouter, WebSocket, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect

from core.broker.redis import redis
from core.db.models import Chat
from crud.chat import ChatRepository
from crud.message import MessageRepository
from deps import get_current_user, get_db

router = APIRouter()

# Авторизация и получение беарер токена, чтобы потом захардкодить в код выше (UPD: хардкод не токена, а логин + пароль)
"""
var xhr = new XMLHttpRequest();
var body = 'username=user&password=user';
xhr.open("POST", '/login/token', true);
xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
xhr.send(body);
xhr.onreadystatechange = function() { 
    console.log(this.responseText);
    localStorage.setItem("jwtoken", re)
}
"""


@router.get("/ws-page")
async def ws_page():
    with open('endpoints/resources/page.html', 'r') as page:
        return HTMLResponse(page.read())


async def get_current_user_ws(websocket: WebSocket):  # , user_id: int = Depends(get_current_user)):
    if 'cookie' in websocket.headers:
        c = websocket.headers['cookie']
        if c and c.startswith('Authorization=Bearer '):
            token = c.replace('Authorization=Bearer ', "")
            logging.error(f"!TOKEN {token}")
            return await get_current_user(token=token)


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket,
                             chat_id, user_id: int = Depends(get_current_user_ws), db: Session = Depends(get_db)):
    logging.error(f"!!!!!!!!!!NEW CLIENT!!!!!!!!!!!!!!")
    logging.error(f"!!!!!!!!!!USER {user_id}!!!!!!!!!!!!!!")
    logging.error(websocket.headers)

    chat: Chat = ChatRepository().find_by_id(db=db, id=chat_id)

    await websocket.accept()
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"chat-{chat_id}")
    await websocket.send_text(f"Чат {chat.title}, описание: {chat.description}")

    messages = MessageRepository().get_last_messages(chat_id=chat_id, db=db, limit=10)
    if messages:
        await websocket.send_text(f"Последние сообщения:")
        for m in messages[::-1]:
            await websocket.send_text(f"User {m.user_id} says: {m.text}")
    await websocket.send_text(f"Новые сообщения:")
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                data = json.loads(bytes(message['data']).decode().replace('\'', '\"'))
                logging.error(data)
                await websocket.send_text(f"User {data['user_id']} says: {data['text']}")
    except WebSocketDisconnect:  # не работает...
        await websocket.send_text("Disconnect")
        await redis.publish(f"chat-{chat_id}", str({'text': "Bye bye!", 'user_id': 'Неизвестный'}))


@router.get("/ws-pubsub")
async def ws_pubsub(user_id: int = Depends(get_current_user),
                    db: Session = Depends(get_db),
                    chat_id: int = 2,
                    text: str = "test text"):
    await redis.publish(f"chat-{chat_id}", str({'text': text, 'user_id': user_id}))
    MessageRepository().create(db=db, text=text, user_id=user_id, chat_id=chat_id)
