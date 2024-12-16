from db.connect import session
from db.create_tables import User, Note

# Создаёт заметку
def create_note(title: str, content:str, user_id: int):
    new_note = Note(title=title, content=content, user_id=user_id)
    session.add(new_note)
    session.commit()
    return new_note

# Получаем все заметки пользователя по айди пользователя
def get_all_user_notes(user_id: int):
    notes_list = session.query(Note).filter_by(
        user_id=user_id,
    ).all()
    return notes_list

def delete_note(note_id: int):
    note = session.query(Note).filter_by(
        id=note_id,
    ).one_or_none()
    if note:
        session.delete(note)
        session.commit()
        return True
    return False

def update_note(note_id: int , title: str, content: str):
    note = session.query(Note).filter_by(
        id=note_id
    ).one_or_none()
    if not note:
        return None
    note.title = title
    note.content = content
    session.commit()

def get_note_by_id(note_id: int):
    note = session.query(Note).filter_by(
        id=note_id,
    ).one_or_none()
    return note

# Примеры
# evgen_note = create_note("my note title", "content maker", 3)
# notes = get_all_user_notes(3)
# update_note(1, title="111", content="222")
# delete_note(2)
# print(notes)
# note = get_note_by_id(3)
