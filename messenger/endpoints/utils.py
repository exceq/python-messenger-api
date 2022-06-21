"""Различные методы проверки функционала"""
import json
import logging

from fastapi import APIRouter, WebSocket, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect

from core.broker.redis import redis
from crud.message import MessageRepository
from deps import get_current_user, get_db

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Chat ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="connectToChat(event)">
            <input type="text" id="chat_id" autocomplete="off"/>
            <button>Connect</button>
        </form>
        <br>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws;
            var user_id;
            var xhr = new XMLHttpRequest();
            var body = 'username=user&password=user';
            xhr.open("POST", '/login/token', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.send(body);
            xhr.onreadystatechange = function() { 
                console.log(this.responseText);
                if (this.readyState != 4) return;
            
                var resp = JSON.parse(this.response);
                localStorage.setItem("jwttoken", resp['access_token']);
            }
            
            function sendMessage(event) {
                if (!ws || !user_id) {
                    console.log("null");
                    event.preventDefault();
                    return;
                }
                
                var input = document.getElementById("messageText");
                ws.send(input.value);
                input.value = '';
                event.preventDefault();
            };        
            function connectToChat(event) {
                var chat_id = document.getElementById("chat_id").value;
                
                document.querySelector("#ws-id").textContent = chat_id;
                ws = new WebSocket(`ws://localhost:8080/utils/ws/${chat_id}`);
                ws.onmessage = function(event) {
                    console.log(event.data);
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                };

                event.preventDefault();
            }
            function sendMessage(event)
            {
                try {
                    var chat_id = document.getElementById("chat_id").value;
                    var input = document.getElementById("messageText").value;
                    var xmlHttp = new XMLHttpRequest();
                    xmlHttp.open("GET", `/utils/ws-pubsub?chat_id=${chat_id}&text=${input}`, true); // true for asynchronous 
                    xmlHttp.setRequestHeader('Authorization', `Bearer ${localStorage.getItem("jwttoken")}`);
                    xmlHttp.send();
                } catch (err) {                
                  console.log(err);                
                }
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""  # несколько клиентов

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
    return HTMLResponse(html)


async def get_current_user_ws(websocket: WebSocket): #, user_id: int = Depends(get_current_user)):
    c = websocket.headers['cookie']
    if c and c.startswith('Authorization=Bearer '):
        token = c.replace('Authorization=Bearer ', "")
        logging.error(f"!TOKEN {token}")
        return await get_current_user(token=token)


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket,
                             chat_id, user_id: int = Depends(get_current_user_ws)):
    logging.error(f"!!!!!!!!!!NEW CLIENT!!!!!!!!!!!!!!")
    logging.error(f"!!!!!!!!!!USER {user_id}!!!!!!!!!!!!!!")
    logging.error(websocket.headers)
    await websocket.accept()
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"chat-{chat_id}")

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
