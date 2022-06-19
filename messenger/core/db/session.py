from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")
DB_PORT = getenv("DB_PORT")

db_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:{DB_PORT}/{POSTGRES_DB}"
engine = create_engine(db_url, echo='debug')
session = sessionmaker(engine)
