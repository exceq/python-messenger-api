from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
DB_NAME = getenv("DB_NAME")
DB_PORT = getenv("DB_PORT")

db_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url)
session = sessionmaker(engine)
