from db.connect import session
from db.create_tables import User, Session

# Создаёт заметку
def create_session(user_id: int):
    new_session = Session(user_id=user_id, is_active=True)
    session.add(new_session)
    session.commit()
    return new_session

def get_session():
    active_session = session.query(Session).filter_by(
        is_active=True,
    ).order_by(Session.id.desc()).first()
    return active_session

def deactivate_sessions():
    active_sessions = session.query(Session).filter_by(
        is_active=True,
    ).all()
    if active_sessions:
        for user_session in active_sessions:
            user_session.is_active = False
            user_session.commit()
    return True
