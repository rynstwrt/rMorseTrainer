import sys
from string import ascii_uppercase
import random
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QMainWindow,
    QComboBox,
    QLabel,
    QWidget,
    QPushButton
)
from qt_material import apply_stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("rMorseTrainer")

        container_widget = QWidget()
        layout = QVBoxLayout()
        container_widget.setLayout(layout)
        self.setCentralWidget(container_widget)

        included_items_form = QFormLayout()
        included_items_label = QLabel("To practice:")
        included_items_combo_box = QComboBox()
        included_items_combo_box.addItems(["Letters Only", "Numbers Only", "Both Letters and Numbers"])
        included_items_form.addRow(included_items_label, included_items_combo_box)
        layout.addLayout(included_items_form)

        speed_form = QFormLayout()
        speed_label = QLabel("Speed:")
        speed_combo_box = QComboBox()
        speed_combo_box.addItems(["10 wpm", "20 wpm", "30 wpm", "40 wpm"])
        speed_form.addRow(speed_label, speed_combo_box)
        layout.addLayout(speed_form)

        self.play_button = QPushButton("Play Sample")
        self.play_button.clicked.connect(self.on_play_button_pressed)
        layout.addWidget(self.play_button)

        self.letter_options_text = QLabel("Select which letter that was:")
        self.letter_options_text.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.letter_options_text.setVisible(False)
        layout.addWidget(self.letter_options_text)
        self.letter_options_container = QHBoxLayout()
        self.letter1 = QPushButton()
        self.letter2 = QPushButton()
        self.letter3 = QPushButton()
        self.letter4 = QPushButton()
        self.letter5 = QPushButton()
        self.letter_options = [self.letter1, self.letter2, self.letter3, self.letter4, self.letter5]
        for letter_button in self.letter_options:
            self.letter_options_container.addWidget(letter_button)
            letter_button.clicked.connect(lambda: self.on_choice_clicked(letter_button.text()))
            letter_button.setVisible(False)
        layout.addLayout(self.letter_options_container)


    def on_play_button_pressed(self):
        if self.play_button.text() == "Play Sample":
            self.play_button.setText("Play Next Sample")

            self.letter_options_text.setVisible(True)

            for letter_button in self.letter_options:
                letter_button.setVisible(True)

        answer = random.choice(ascii_uppercase)

        choices = self.generate_option_choices(answer)
        for i, letter_button in enumerate(self.letter_options):
            letter_button.setText(choices[i])

        self.play_letter_sound(answer)


    def play_letter_sound(self, letter):
        print(letter)


    def on_choice_clicked(self, choice):
        print(choice)


    def generate_option_choices(self, answer):
        randomly_generated = [""] * len(self.letter_options)
        for i in range(len(self.letter_options)):
            randomly_generated[i] = random.choice(ascii_uppercase)
        answer_index = random.randint(1, len(self.letter_options) - 1)
        randomly_generated[answer_index] = answer
        return randomly_generated



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    apply_stylesheet(app, theme="dark_cyan.xml")
    window.setStyleSheet("QLabel { font-size: 15px; text-transform: uppercase; }")
    window.show()
    app.exec()