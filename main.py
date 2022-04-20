from fastapi import FastAPI
from endpoints.user import router as user_router

app = FastAPI()

app.include_router(user_router, prefix='/user', tags=['User'])


@app.get('/')
async def hello():
    return {'message': 'Hello world!'}
