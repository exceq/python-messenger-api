from sqlalchemy.orm import Session

from core.db.models import User
from schemas.user import UserModel


def create(user_model: UserModel, db: Session):
    user_db = User(**user_model.dict())
    db.add(user_db)
    db.commit()
    return user_db


def find_by_id(user_id: int, db: Session):
    return db.query(User).filter_by(id=user_id).one_or_none()


def delete(user_id: int, db: Session):
    deleted = db.query(User).filter_by(id=user_id).delete()
    db.commit()
    return deleted


def update(user_id: int, user_model: UserModel, db: Session):
    user = db.query(User).filter_by(id=user_id).one_or_none()
    for k, v in user_model.dict().items():
        setattr(user, k, v)
    db.commit()
    return user
