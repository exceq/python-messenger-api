from fastapi import FastAPI
from endpoints.user import router as user_router

app = FastAPI()

app.include_router(user_router, prefix='/user', tags=['User'])


@app.get('/')
async def hello():
    return {'message': 'Hello world!'}

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
