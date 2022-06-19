from sqlalchemy.orm import Session

from core.db.models import Chat, User, Message
from crud.crud_repository import Crud
from crud.message import MessageRepository
from crud.user import UserRepository
from schemas.chat import ChatModel

user_repository = UserRepository()


class ChatRepository(Crud):
    def __init__(self):
        super().__init__(Chat)

    def create_chat(self, db: Session, chat_model: ChatModel, creator_user_id: int):
        chat_db = Chat(**chat_model.dict())
        chat_db.creator_user_id = creator_user_id
        chat_db.users = [user_repository.find_by_id(creator_user_id, db=db)]
        db.add(chat_db)
        db.commit()
        return chat_db

    def add_user_to_chat(self, chat_id: int, user_id: int, db: Session):
        chat = self.find_by_id(id=chat_id, db=db)
        user = user_repository.find_by_id(id=user_id, db=db)
        chat.users += [user]
        db.commit()
        return chat

    def get_last_active_chats(self, user_id: int, db: Session):
        user: User = UserRepository().find_by_id(id=user_id, db=db)

        messages = [MessageRepository().get_last_messages(chat_id=chat.id, db=db, limit=1)[0] for chat in user.chats]
        messages.sort(key=lambda x: x.created, reverse=True)

        chats = list(map(lambda m: db.query(Chat).filter_by(id=m.chat_id).one(), messages))
        return chats
