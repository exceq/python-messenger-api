from sqlalchemy.orm import Session

import security
from core.db.models import User
from crud.crud_repository import Crud


class UserRepository(Crud):
    def __init__(self):
        super().__init__(User)

    def create_from_model(self, db: Session, **model_params):
        print(model_params)
        if 'password' in model_params and 'hashed_password' not in model_params:
            model_params['hashed_password'] = security.get_password_hash(model_params['password'])
            model_params.pop('password')
        return super(UserRepository, self).create(db=db, entity=model_params)

    def authenticate(self, login: str, password: str, db: Session):
        user = self.find_by_login(login=login, db=db)
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None
        return user

    def find_by_login(self, login: str, db: Session):
        return db.query(User).filter_by(login=login).one_or_none()
