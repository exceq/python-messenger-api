from sqlalchemy.orm import Session

from core.db.models import Chat
from crud.crud_repository import Crud
from crud.user import UserRepository
from schemas.chat import ChatModel

user_repository = UserRepository()


class ChatRepository(Crud):
    def __init__(self):
        super().__init__(Chat)

    def create_from_model(self, db: Session, chat_model: ChatModel):
        chat_db = Chat(**chat_model.dict())
        chat_db.users = [user_repository.find_by_id(chat_model.creator_user_id, db=db)]
        db.add(chat_db)
        db.commit()
        return chat_db

    def add_user_to_chat(self, chat_id: int, user_id: int, db: Session):
        chat = self.find_by_id(id=chat_id, db=db)
        user = user_repository.find_by_id(id=user_id, db=db)
        chat.users += [user]
        db.commit()
        return chat
