import random as rnd
import string as str
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys

# creating password
class CreatePassword:
    def __init__(self, minlen=4, maxlen=20):
        self.min = minlen
        self.max = maxlen

    def generate(self, length, use_upper, use_lower, use_digits, use_special):
        char_pool = ""
        if use_upper:
            char_pool += str.ascii_uppercase
        if use_lower:
            char_pool += str.ascii_lowercase
        if use_digits:
            char_pool += str.digits
        if use_special:
            char_pool += str.punctuation

        if not char_pool:
            raise ValueError("No character sets selected!")

        return ''.join(rnd.choices(char_pool, k=length))

# GUI
class QApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🔐 Password Generator")
        self.setGeometry(200, 200, 500, 420)

        self.generator = CreatePassword()

        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.title = QLabel("🎯 Generate a Secure Password")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title)

        self.password_field = QLineEdit()
        self.password_field.setReadOnly(True)
        self.password_field.setPlaceholderText("Your password will appear here...")
        self.password_field.setStyleSheet("font-size: 16px; padding: 5px;")
        layout.addWidget(self.password_field)

        self.copy_button = QPushButton("📋 Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)

        self.uppercase_cb = QCheckBox("Include UPPERCASE letters (A-Z)")
        self.uppercase_cb.setChecked(True)
        layout.addWidget(self.uppercase_cb)

        self.lowercase_cb = QCheckBox("Include lowercase letters (a-z)")
        self.lowercase_cb.setChecked(True)
        layout.addWidget(self.lowercase_cb)

        self.digits_cb = QCheckBox("Include numbers (0-9)")
        self.digits_cb.setChecked(True)
        layout.addWidget(self.digits_cb)

        self.special_cb = QCheckBox("Include symbols (!@#$...)")
        self.special_cb.setChecked(True)
        layout.addWidget(self.special_cb)

        self.length_label = QLabel("Length: 12")
        layout.addWidget(self.length_label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(self.generator.min)
        self.slider.setMaximum(self.generator.max)
        self.slider.setValue(12)
        self.slider.valueChanged.connect(self.update_slider_label)
        layout.addWidget(self.slider)

        self.generate_button = QPushButton("🔄 Generate Password")
        self.generate_button.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)
        self.show()

    def update_slider_label(self, value):
        self.length_label.setText(f"Length: {value}")

    def generate_password(self):
        length = self.slider.value()
        try:
            password = self.generator.generate(
                length,
                self.uppercase_cb.isChecked(),
                self.lowercase_cb.isChecked(),
                self.digits_cb.isChecked(),
                self.special_cb.isChecked()
            )
            self.password_field.setText(password)
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def copy_to_clipboard(self):
        password = self.password_field.text()
        if password.strip() == "":
            QMessageBox.information(self, "No password", "Please generate a password first.")
            return
        QApplication.clipboard().setText(password)
        QMessageBox.information(self, "Copied", "Password copied to clipboard!")

# running the app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QApp()
    sys.exit(app.exec())