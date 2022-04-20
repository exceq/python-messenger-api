from datetime import datetime

from pydantic import BaseModel


class UserModel(BaseModel):
    login: str
    password: str
    name: str


class User(UserModel):
    id: int
    active: bool
    updated: datetime
    created: datetime
