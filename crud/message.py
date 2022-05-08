from core.db.models import Message
from crud.crud_repository import Crud


class MessageRepository(Crud):
    def __init__(self):
        super().__init__(Message)
