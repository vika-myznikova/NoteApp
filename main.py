import re
import sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTextEdit, QListWidget, QHBoxLayout
)


class RegistrationWindow(QWidget):
    def __init__(self, users_db):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setGeometry(400, 400, 400, 300)
        self.setStyleSheet("background-color: #F7F7F7; font-family: Arial;")
        self.users_db = users_db  # База данных

        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Создайте аккаунт")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: black")
        layout.addWidget(title)

        # Поля ввода
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")
        self.username_input.setStyleSheet("padding: 10px; border: 1px solid #CCCCCC; border-radius: 5px;")

        self.password_input = QLineEdit()

        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setStyleSheet("padding: 10px; border: 1px solid #CCCCCC; border-radius: 5px;")

        # Кнопка регистрации
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.setStyleSheet("""
            background-color: #4CAF50; 
            color: white; 
            padding: 10px; 
            border: none; 
            border-radius: 5px; 
            font-size: 16px;
        """)
        self.register_button.clicked.connect(self.register)

        # Кнопка входа
        self.login_button = QPushButton("Войти")
        self.login_button.setStyleSheet("""
            background-color: #2196F3; 
            color: white; 
            padding: 10px; 
            border: none; 
            border-radius: 5px; 
            font-size: 16px;
        """)
        self.login_button.clicked.connect(self.open_login_window)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Проверка
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Проверка
        if re.search(r'[а-яА-ЯЁё]', username) or re.search(r'[а-яА-ЯЁё]', password):
            QMessageBox.warning(self, "Ошибка", "Русские буквы использовать нельзя в логине и пароле.")
            return

        # Проверка
        if re.search(
                r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F900-\U0001F9FF]',
                username) or \
                re.search(
                    r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F900-\U0001F9FF]',
                    password):
            QMessageBox.warning(self, "Ошибка", "Смайлы и эмодзи не допускаются в логине и пароле.")
            return

        # Проверка
        if username == password:
            QMessageBox.warning(self, "Ошибка", "Логин и пароль не должны совпадать.")
            return

        # Проверка
        if len(username) < 9 or len(username) > 16:
            QMessageBox.warning(self, "Ошибка", "Логин должен содержать от 9 до 16 символов.")
            return

        # Проверка
        if not (8 <= len(password) <= 16):
            QMessageBox.warning(self, "Ошибка", "Пароль должен содержать от 8 до 16 символов.")
            return

        # Проверка
        if not re.search("[a-zA-Z]", password) or not re.search("[!@#$%^&*]", password):
            QMessageBox.warning(self, "Ошибка", "Пароль должен включать хотя бы одну букву и один специальный символ.")
            return

        # Проверка
        if username in self.users_db:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким именем уже существует.")
        else:
            self.users_db[username] = password  # Сохранение данных
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
            self.close()
            self.main_window = MainWindow()  # Создание основного окна
            self.main_window.show()  # Открытие

    def open_login_window(self):
        self.close()
        self.login_window = LoginWindow(self.users_db)
        self.login_window.show()  # Открытие окна входа


class LoginWindow(QWidget):
    def __init__(self, users_db):
        super().__init__()
        self.setWindowTitle("Вход")
        self.setGeometry(400, 400, 400, 300)
        self.setStyleSheet("background-color: #F7F7F7; font-family: Arial;")

        self.users_db = users_db  # База данных

        layout = QVBoxLayout()

        title = QLabel("Вход в систему")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")
        self.username_input.setStyleSheet("padding: 10px; border: 1px solid #CCCCCC; border-radius: 5px;")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setStyleSheet("padding: 10px; border: 1px solid #CCCCCC; border-radius: 5px;")

        self.login_button = QPushButton("Войти")
        self.login_button.setStyleSheet("""
            background-color: #4CAF50; 
            color: white; 
            padding: 10px; 
            border: none; 
            border-radius: 5px; 
            font-size: 16px;
        """)
        self.login_button.clicked.connect(self.login)

        self.return_button = QPushButton("Вернуться к регистрации")
        self.return_button.setStyleSheet("""
            background-color: #2196F3; 
            color: white; 
            padding: 10px; 
            border: none; 
            border-radius: 5px; 
            font-size: 16px;
        """)
        self.return_button.clicked.connect(self.open_registration_window)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.return_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:  # Проверка
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return  # Выход если поля пустые

        if username in self.users_db and self.users_db[username] == password:
            QMessageBox.information(self, "Успех", "Вы успешно вошли в систему!")
            self.close()
            self.main_window = MainWindow()  # Создание окна

            self.main_window.show()  # Открытие окна
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль.")

    def open_registration_window(self):
        self.close()  # Закрытие окна
        self.registration_window = RegistrationWindow(self.users_db)
        self.registration_window.show()  # Открытие окна


class NoteEditorWindow(QWidget):
    def __init__(self, note, on_save, on_delete):
        super().__init__()
        self.note = note  # Заголовок и содержимое
        self.on_save = on_save
        self.on_delete = on_delete

        self.setWindowTitle("Редактирование заметки")
        self.setGeometry(500, 500, 400, 300)
        self.setStyleSheet("background-color: #F7F7F7; font-family: Arial;")

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setText(note[0])  # Заголовок заметки
        self.title_input.setPlaceholderText("Заголовок заметки")
        self.title_input.setStyleSheet("padding: 10px; border: 1px solid #CCCCCC; border-radius: 5px;")

        self.content_text = QTextEdit()
        self.content_text.setText(note[1])  # Текст заметки
        self.content_text.setPlaceholderText("Содержимое заметки...")
        self.content_text.setStyleSheet("""
            padding: 10px; 
            border: 1px solid #CCCCCC; 
            border-radius: 5px; 
            background-color: white;
        """)

        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Сохранить")
        self.save_button.setStyleSheet("""
            background-color: #4CAF50;

            color: white; 
            padding: 10px; 
            border: none; 
            border-radius: 5px; 
            font-size: 16px;
        """)
        self.save_button.clicked.connect(self.save_note)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setStyleSheet("""
            background-color: #F44336; 
            color: white; 
            padding: 10px; 
            border: none; 
            border-radius: 5px; 
            font-size: 16px;
        """)
        self.delete_button.clicked.connect(self.delete_note)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.delete_button)

        layout.addWidget(self.title_input)
        layout.addWidget(self.content_text)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_note(self):
        title = self.title_input.text()
        content = self.content_text.toPlainText()
        self.on_save(title, content)
        self.close()  # Закрыть

    def delete_note(self):
        response = QMessageBox.question(self, "Удалить заметку", "Вы уверены, что хотите удалить эту заметку?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if response == QMessageBox.StandardButton.Yes:
            self.on_delete()  # Удалить
            self.close()  # Закрыть


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заметки")
        self.setGeometry(400, 400, 400, 600)
        self.setStyleSheet("background-color: #F7F7F7; font-family: Arial;")
        self.notes = []  # Список

        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Мои заметки")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Заметки
        self.notes_list = QListWidget()
        self.notes_list.setStyleSheet("border: none; padding: 5px;")
        self.notes_list.itemDoubleClicked.connect(self.edit_note)  # Редактирование
        layout.addWidget(self.notes_list)

        # Кнопка заметки
        self.new_note_button = QPushButton("Новая заметка")
        self.new_note_button.setStyleSheet("""
            background-color: #2196F3; 
            color: white; 
            padding: 10px; 
            border: none; 
            border-radius: 5px; 
            font-size: 16px;
        """)
        self.new_note_button.clicked.connect(self.new_note)
        layout.addWidget(self.new_note_button)

        self.setLayout(layout)

    def new_note(self):
        self.open_note_editor(("", ""), self.add_note)

    def edit_note(self, item):
        note_index = self.notes_list.currentRow()
        note = self.notes[note_index]
        self.open_note_editor(note, self.update_note)

    def open_note_editor(self, note, on_save):
        self.note_editor = NoteEditorWindow(note, on_save, lambda: self.delete_note(self.notes_list.currentRow()))
        self.note_editor.show()

    def add_note(self, title, content):
        self.notes.append((title, content))
        self.notes_list.addItem(title)  # Добавление заголовка

    def update_note(self, title, content):
        note_index = self.notes_list.currentRow()
        self.notes[note_index] = (title, content)
        self.notes_list.currentItem().setText(title)  # Обновление заголовка

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]
            self.notes_list.takeItem(index)  # Удаление из списка


if __name__ == "__main__":
    app = QApplication(sys.argv)
    users_db = {}  # Создание базы данных
    registration_window = RegistrationWindow(users_db)
    registration_window.show()  # Показать окно
    sys.exit(app.exec())

