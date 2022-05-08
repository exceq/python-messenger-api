from core.db.models import Message
from crud.crud_repository import Crud


class MessageRepository(Crud):
    def __init__(self):
        super().__init__(Message)


def get_all_byq_chat_id(chat_id: int):
    return filter(lambda message: message.chat_id == chat_id, message_database)

