from schemas.message import MessageModel, Message
from datetime import datetime

message_database = []


def create(message_model: MessageModel):
    new_message = Message(id=len(message_database) + 1, created=datetime.now(), **message_model.dict())
    message_database.append(new_message)
    return new_message


def get(message_id: int):
    return message_database[message_id - 1]


def delete(message_id: int):
    return 1


def update(message_id: int, message_model: MessageModel):
    message = get(message_id)
    message.updated = datetime.now()
    message.text = message_model.text
    return message


def get_all_byq_chat_id(chat_id: int):
    return filter(lambda message: message.chat_id == chat_id, message_database)

