from sqlalchemy.orm import Session

from core.db.models import Chat
from schemas.chat import ChatModel
import crud.user as user_repository


def create(chat_model: ChatModel, db: Session):
    chat_db = Chat(**chat_model.dict())
    chat_db.users = [user_repository.find_by_id(chat_model.creator_user_id, db=db)]
    db.add(chat_db)
    db.commit()
    return chat_db


def find_by_id(chat_id: int, db: Session):
    return db.query(Chat).filter_by(id=chat_id).one_or_none()


def delete(chat_id: int, db: Session):
    deleted = db.query(Chat).filter_by(id=chat_id).delete()
    db.commit()
    return deleted


def update(chat_id: int, chat_model: ChatModel, db: Session):
    chat = db.query(Chat).filter_by(id=chat_id).one_or_none()
    for k, v in chat_model.dict().items():
        setattr(chat, k, v)
    db.commit()
    return chat


def add_user_to_chat(chat_id: int, user_id: int, db: Session):
    chat = find_by_id(chat_id=chat_id, db=db)
    user = user_repository.find_by_id(user_id=user_id, db=db)
    chat.users += [user]
    db.commit()
    return chat
