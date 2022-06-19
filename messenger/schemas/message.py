from datetime import datetime

from pydantic import BaseModel


class MessageModel(BaseModel):
    chat_id: int
    text: str


class MessageModelAsync(MessageModel):
    user_id: int
    delay_in_seconds: int = 0


class Message(MessageModel):
    id: int
    user_id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True
