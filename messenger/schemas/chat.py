from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.chat_type import ChatType


class ChatModel(BaseModel):
    title: str
    description: Optional[str] = None
    chat_type: ChatType


class Chat(ChatModel):
    id: int
    creator_user_id: int
    created: datetime
    updated: datetime
    users: list

    class Config:
        orm_mode = True