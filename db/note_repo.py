from db.connect import session
from db.create_tables import User, Note

# Создаёт заметку
def create_note(title: str, content:str, user_id: int):
    new_note = Note(title=title, content=content, user_id=user_id)
    session.add(new_note)
    session.commit()

# Получаем все заметки пользователя по айди пользователя
def get_all_user_notes(user_id: int):
    notes_list = session.query(Note).filter_by(
        user_id=user_id,
    ).all()
    return notes_list

# Примеры
# evgen_note = create_note("my note title", "content maker", 1)
# notes = get_all_user_notes(1)
