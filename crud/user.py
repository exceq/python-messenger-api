from datetime import datetime

from schemas.user import User, UserModel

user_database = [
    User(id=1, active=True, created=datetime(2020, 4, 17, 0, 0, 5), login='ivan', password='ivan', name='Иван'),
    User(id=2, active=True, created=datetime(2022, 3, 16, 12, 12, 59), login='dima', password='dima', name='Дмитрий')
]


def create(user_model: UserModel):
    new_user = User(id=len(user_database) + 1, created=datetime.now(), active=True, **user_model.dict())
    user_database.append(new_user)
    return new_user


def get(user_id: int):
    return user_database[user_id - 1]


def delete(user_id: int):
    user = get(user_id)
    user.active = False
    user.updated = datetime.now()
    return


def update(user_id: int, user_model: UserModel):
    user = get(user_id)
    for k, v in user_model.dict().items():
        user[k] = v
    user.updated = datetime.now()
    return user
