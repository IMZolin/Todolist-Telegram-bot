from peewee import fn

from models import User
from utils.misc.logging import logger


def count_tasks(user) -> int:
    query = User.get_or_none(User.id == user.id).select(fn.COUNT(User.id))
    return query.scalar()


def get_tasks() -> list[User]:
    query = User.select()

    return list(query)


def get_task(id: int) -> User:
    return User.get_or_none(User.id == id)


def update_task(user: User, name: str, username: str = None) -> User:
    user.name = name
    user.username = username
    user.save()

    return user


def edit_user_language(id: int, language: str):
    query = User.update(language=language).where(User.id == id)
    query.execute()


def create_user(id: int, name: str, username: str = None, language: str = None) -> User:
    new_user = User.create(id=id, name=name, username=username, language=language)

    new_user.is_admin = False
    new_user.save()

    logger.info(f'New user {new_user}')

    return new_user


def get_or_create_task(id: int, name: str, username: str = None, language: str = None) -> User:
    user = get_task(id)

    if user:
        user = update_task(user, name, username)

        return user

    return create_user(id, name, username, language)
