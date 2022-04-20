from datetime import datetime

from pydantic import BaseModel

from schemas.chat_type import ChatType


class ChatModel(BaseModel):
    chat_type: ChatType


class Chat(ChatModel):
    id: int
    created: datetime
    updated: datetime
