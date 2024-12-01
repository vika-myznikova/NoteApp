from db.connect import session
from db.create_tables import User


def create_user(username: str, password: str):
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()

def get_user(username: str, password: str):
    user = session.query(User).filter_by(
        username=username,
        password=password
    ).one_or_none()
    return user

i = get_user("evgen", "228322")
