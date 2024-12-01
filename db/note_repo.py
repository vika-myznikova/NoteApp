from db.connect import session
from db.create_tables import User, Note

def create_note(title: str, content:str, user_id: int):
    new_note = Note(title=title, content=content, user_id=user_id)
    session.add(new_note)
    session.commit()

def get_all_user_notes(user_id: int):
    notes_list: list = Note(user_id)
