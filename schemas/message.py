from datetime import datetime

from pydantic import BaseModel


class MessageModel(BaseModel):
    user_id: int
    chat_id: int
    text: str


class MessageModelAsync(MessageModel):
    send_datetime: datetime = datetime.now()


class Message(MessageModel):
    id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True
