from celery.utils.log import get_task_logger

from core.broker.celery import celery_app
from core.db.session import session
from crud.message import MessageRepository
from crud.user import UserRepository

user_repository = UserRepository()
message_repository = MessageRepository()
logger = get_task_logger(__name__)


@celery_app.task(name="queue.send_async")
def send_async(**kwargs):
    d = kwargs
    d.pop('delay_in_seconds')
    with session() as db:
        return message_repository.create(db=db, **d)
