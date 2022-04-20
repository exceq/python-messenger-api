from datetime import datetime

from schemas.chat import ChatModel, Chat
from schemas.chat_response import ChatResponse
from schemas.chat_type import ChatType
from schemas.chat_user import ChatUser
import crud.message as message_repository

chat_database = [
    Chat(id=1, created=datetime(2022, 4, 20, 0, 0, 0), chat_type=ChatType.private)
]

chat_user_chat_database = [
    ChatUser(user_id=1, chat_id=1),
    ChatUser(user_id=2, chat_id=1)
]


def create(user_id: int, chat_model: ChatModel):
    chat = Chat(id=len(chat_database) + 1, created=datetime.now, **chat_model.dict())
    chat_database.append(chat)

    chat_user = ChatUser(user_id=user_id, chat_id=chat.id)
    chat_user_chat_database.append(chat_user)

    return chat


def get(chat_id: int):


    resp = ChatResponse()

    return chat_database[user_id - 1]


def delete(user_id: int):
    return 1


def update(user_id: int, user_model: User):
    user = get(user_id)
    for k, v in user_model.dict().values():
        user[k] = v
