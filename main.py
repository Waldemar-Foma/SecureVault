import sys
import re
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt

class PasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SecureVault - Менеджер Паролей")
        self.setGeometry(100, 100, 800, 600)

        with open("resources/styles.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.init_ui()

    def init_ui(self):
        self.title_label = QLabel("Добро пожаловать в SecureVault", self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.service_label = QLabel("Сервис:", self)
        self.layout.addWidget(self.service_label)

        self.service_input = QLineEdit(self)
        self.service_input.setPlaceholderText("Введите адрес сервиса")
        self.layout.addWidget(self.service_input)

        self.username_label = QLabel("Логин:", self)
        self.layout.addWidget(self.username_label)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Введите логин")
        self.layout.addWidget(self.username_input)

        self.password_label = QLabel("Пароль:", self)
        self.layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Изначально скрываем пароль
        self.layout.addWidget(self.password_input)

        self.toggle_button = QPushButton("Показать пароль", self)
        self.toggle_button.clicked.connect(self.toggle_password_visibility)
        self.layout.addWidget(self.toggle_button)

        self.password_strength_label = QLabel("", self)
        self.password_strength_label.setStyleSheet("color: red;")
        self.layout.addWidget(self.password_strength_label)

        self.add_button = QPushButton("Добавить пароль", self)
        self.add_button.clicked.connect(self.add_password)
        self.layout.addWidget(self.add_button)

        self.password_table = QTableWidget(self)
        self.password_table.setColumnCount(3)
        self.password_table.setHorizontalHeaderLabels(["Сервис", "Логин", "Пароль"])
        self.layout.addWidget(self.password_table)

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_button.setText("Скрыть пароль")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_button.setText("Показать пароль")

    def add_password(self):
        service = self.service_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if not service or not username or not password:
            self.show_error_message("Все поля должны быть заполнены.")
            return

        if not self.check_password_strength(password):
            return  # Не продолжаем добавление пароля, если он не соответствует критериям

        row_position = self.password_table.rowCount()
        self.password_table.insertRow(row_position)
        self.password_table.setItem(row_position, 0, QTableWidgetItem(service))
        self.password_table.setItem(row_position, 1, QTableWidgetItem(username))
        self.password_table.setItem(row_position, 2, QTableWidgetItem(password))

        self.service_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.password_strength_label.clear()

    def check_password_strength(self, password):
        if len(password) < 8:
            self.password_strength_label.setText("Пароль слишком короткий. Минимум 8 символов.")
            return False
        if not re.search(r'[A-Z]', password):
            self.password_strength_label.setText("Пароль должен содержать хотя бы одну заглавную букву.")
            return False
        if not re.search(r'[0-9]', password):
            self.password_strength_label.setText("Пароль должен содержать хотя бы одну цифру.")
            return False
        if not re.search(r'[@$!%*?&]', password):
            self.password_strength_label.setText("Пароль должен содержать хотя бы один специальный символ.")
            return False
        self.password_strength_label.clear()
        return True

    def show_error_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("Ошибка")
        msg_box.setText(message)

        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #e74c3c;
            }
            QLabel {
                color: white;
            }
        """)

        msg_box.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PasswordManager()
    window.show()

    sys.exit(app.exec())
