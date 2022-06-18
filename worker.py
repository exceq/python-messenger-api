from celery.utils.log import get_task_logger

from core.broker.celery import app
from core.db.session import session
from crud.user import UserRepository
from crud.message import MessageRepository
from schemas.message import MessageModelAsync
from schemas.user import UserModelCreate

user_repository = UserRepository()
message_repository = MessageRepository()
logger = get_task_logger(__name__)


@app.task(name="test_task")
def hello():
    logger.info("HELLO !!!")
    with session() as db:
        user = UserModelCreate(name='celery', login='celery', password='celery')
        user_repository.create(db=db, entity=user)
        return True


@app.task(name="send_async")
def send_async(message_model: MessageModelAsync):
    with session() as db:
        return message_repository.create(entity=message_model, db=db)
