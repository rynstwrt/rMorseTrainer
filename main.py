import sys
from string import ascii_uppercase
import random
from time import sleep
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtGui import QIcon
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
        self.randomly_generated = None
        self.answer = None
        self.media_player = None
        self.audio_output = None
        self.num_wrong = 0
        self.num_correct = 0
        self.audio_done_playing = True

        self.setWindowTitle("rMorseTrainer")
        self.setWindowIcon(QIcon("assets/rMorseIcon.png"))

        container_widget = QWidget()
        layout = QVBoxLayout()
        container_widget.setLayout(layout)
        self.setCentralWidget(container_widget)

        included_items_form = QFormLayout()
        included_items_label = QLabel("To practice:")
        included_items_combo_box = QComboBox()
        included_items_combo_box.addItems(["Letters Only", "Numbers Only", "Symbols Only", "Letters and Numbers Only", "All"])
        included_items_form.addRow(included_items_label, included_items_combo_box)
        layout.addLayout(included_items_form)

        speed_form = QFormLayout()
        speed_label = QLabel("Speed:")
        speed_combo_box = QComboBox()
        speed_combo_box.addItems(["5 wpm", "12 wpm", "18 wpm", "20 wpm"])
        speed_combo_box.setCurrentIndex(1)
        speed_form.addRow(speed_label, speed_combo_box)
        layout.addLayout(speed_form)

        num_correct_or_wrong_row = QHBoxLayout()
        num_correct_or_wrong_row.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.num_correct_text = QLabel("Correct: 0")
        num_correct_or_wrong_row.addWidget(self.num_correct_text)
        self.num_wrong_text = QLabel("Wrong: 0")
        num_correct_or_wrong_row.addWidget(self.num_wrong_text)
        layout.addLayout(num_correct_or_wrong_row)

        sample_row = QHBoxLayout()
        self.play_button = QPushButton("Play Sample")
        self.play_button.clicked.connect(self.on_play_button_pressed)
        sample_row.addWidget(self.play_button)
        self.replay_button = QPushButton("Replay")
        self.replay_button.clicked.connect(self.on_replay_button_pressed)
        self.replay_button.setEnabled(False)
        sample_row.addWidget(self.replay_button)
        layout.addLayout(sample_row)

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
        for i, letter_button in enumerate(self.letter_options):
            self.letter_options_container.addWidget(letter_button)
            letter_button.setObjectName(str(i))
            letter_button.clicked.connect(self.on_choice_clicked)
            letter_button.setVisible(False)
        layout.addLayout(self.letter_options_container)


    def on_play_button_pressed(self):
        if self.play_button.text() == "Play Sample":
            self.play_button.setText("Play Next Sample")

            self.letter_options_text.setVisible(True)

            for letter_button in self.letter_options:
                letter_button.setVisible(True)

        self.answer = random.choice(ascii_uppercase)
        print("ANSWER: " + self.answer)

        choices = self.generate_option_choices()
        for i, letter_button in enumerate(self.letter_options):
            letter_button.setText(choices[i])
            letter_button.setEnabled(True)

        self.replay_button.setEnabled(True)

        self.play_letter_sound(self.answer)


    def on_replay_button_pressed(self):
        if self.play_button.text() == "Play Sample":
            return

        self.media_player.play()


    def on_audio_state_changed(self, status):
        if status != QMediaPlayer.MediaStatus.EndOfMedia:
            return

        self.audio_done_playing = True


    def play_letter_sound(self, letter):
        file_path = "assets/letter_morse_audio/" + letter.lower() + ".mp3"
        self.play_audio(file_path)


    def on_choice_clicked(self):
        choice_index = self.sender().objectName()
        choice = self.letter_options[int(choice_index)].text()

        if choice != self.answer:
            self.on_wrong()
        else:
            self.on_correct()

        for option_button in self.letter_options:
            option_button.setEnabled(False)

        self.replay_button.setEnabled(False)

    def on_wrong(self):
        self.play_audio("assets/wrong.wav")
        self.num_wrong += 1
        self.num_wrong_text.setText("Wrong: " + str(self.num_wrong))


    def on_correct(self):
        self.play_audio("assets/correct.wav")
        self.num_correct += 1
        self.num_correct_text.setText("Correct: " + str(self.num_correct))


    def play_audio(self, file_path):
        if self.audio_done_playing:

            if self.media_player:
                self.media_player.stop()

            self.media_player = QMediaPlayer()
            self.media_player.mediaStatusChanged.connect(self.on_audio_state_changed)
            self.audio_output = QAudioOutput()
            self.media_player.setAudioOutput(self.audio_output)
            self.media_player.setSource(QUrl.fromLocalFile(file_path))
            self.audio_output.setVolume(50)
            self.media_player.play()

            self.audio_done_playing = False


    def generate_random_option_choices(self):
        self.randomly_generated = [""] * len(self.letter_options)

        for i in range(len(self.letter_options)):
            self.randomly_generated[i] = random.choice(ascii_uppercase)

        answer_index = random.randint(1, len(self.letter_options) - 1)
        self.randomly_generated[answer_index] = self.answer

        return self.randomly_generated


    def generate_option_choices(self):
        random_options = self.generate_random_option_choices()
        while self.has_duplicates(random_options):
            random_options = self.generate_random_option_choices()

        return random_options


    @staticmethod
    def has_duplicates(choices):
        if len(set([x for x in choices if choices.count(x) > 1])) > 0:
            return True
        return False



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    apply_stylesheet(app, theme="dark_cyan.xml")
    window.setStyleSheet("QLabel { font-size: 15px; text-transform: uppercase; }")
    window.show()
    app.exec()