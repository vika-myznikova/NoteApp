from db.connect import session
from db.create_tables import User

# Создать пользователя
def create_user(username: str, password: str):
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()

# Получить пользователя
def get_user(username: str, password: str):
    user = session.query(User).filter_by(
        username=username,
        password=password
    ).one_or_none()
    return user

# Примеры использвания
# i = get_user("evgen", "279823")
# c = create_user("valera", "ga21sz")
# ii = get_user("valera", "ga21sz")
