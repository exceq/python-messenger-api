from os import getenv
from dotenv import load_dotenv

from celery import Celery

load_dotenv()
REDIS_PORT = getenv("REDIS_PORT")

app = Celery('hello', broker=f'redis://localhost:{REDIS_PORT}/0')

