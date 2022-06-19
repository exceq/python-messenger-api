import uvicorn

from fastapi import FastAPI

from core.broker.celery import celery_app
from core.db.models import Base
from core.db.session import engine
from endpoints.chat import router as chat_router
from endpoints.login import router as login_router
from endpoints.message import router as message_router
from endpoints.user import router as user_router
from security import get_password_hash

app = FastAPI()

app.include_router(user_router, prefix='/user', tags=['User'])
app.include_router(chat_router, prefix='/chat', tags=['Chat'])
app.include_router(message_router, prefix='/message', tags=['Message'])
app.include_router(login_router, prefix='/login', tags=['Login'])


@app.get('/')
async def hello():
    return {'message': get_password_hash("user2")}


@app.get('/task')
async def create_task():
    celery_app.send_task(name='test_task')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True, log_level="info")
