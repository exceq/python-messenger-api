from core.db.models import User
from crud.crud_repository import Crud


class UserRepository(Crud):
    def __init__(self):
        super().__init__(User)

