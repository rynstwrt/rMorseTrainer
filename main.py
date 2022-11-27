import sys
from math import ceil
from string import ascii_uppercase
import random
from os import path
from audioplayer import AudioPlayer
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
    QPushButton,
    QGridLayout
)
from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audioplayer = None
        self.answer = None
        self.media_player = None
        self.audio_output = None
        self.num_wrong = 0
        self.num_correct = 0
        self.symbol_list = ["@", ",", ".", "?", "/"]

        self.setWindowTitle("rMorseTrainer")
        self.setWindowIcon(QIcon("assets/rMorseIcon.png"))

        container_widget = QWidget()
        layout = QVBoxLayout()
        container_widget.setLayout(layout)
        self.setCentralWidget(container_widget)

        included_items_form = QFormLayout()
        included_items_label = QLabel("To practice:")
        self.included_items_combo_box = QComboBox()
        self.included_items_combo_box.addItems(["Letters Only", "Numbers Only", "Symbols Only", "Letters and Numbers Only", "All"])
        included_items_form.addRow(included_items_label, self.included_items_combo_box)
        layout.addLayout(included_items_form)

        speed_form = QFormLayout()
        speed_label = QLabel("Speed:")
        self.speed_combo_box = QComboBox()
        self.speed_combo_box.addItems(["25%", "50%", "75%", "100%"])
        self.speed_combo_box.setCurrentIndex(3)
        speed_form.addRow(speed_label, self.speed_combo_box)
        layout.addLayout(speed_form)

        num_correct_or_wrong_row = QHBoxLayout()
        num_correct_or_wrong_row.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.num_correct_text = QLabel("Correct: 0")
        num_correct_or_wrong_row.addWidget(self.num_correct_text)
        self.num_wrong_text = QLabel("Wrong: 0")
        num_correct_or_wrong_row.addWidget(self.num_wrong_text)
        layout.addLayout(num_correct_or_wrong_row)

        sample_row = QHBoxLayout()
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.on_play_button_pressed)
        sample_row.addWidget(self.play_button)
        self.replay_button = QPushButton("Replay")
        self.replay_button.clicked.connect(self.on_replay_button_pressed)
        self.replay_button.setEnabled(False)
        sample_row.addWidget(self.replay_button)
        layout.addLayout(sample_row)

        options_grid = QGridLayout()
        layout.addLayout(options_grid)

        btn_a = QPushButton("A")
        btn_b = QPushButton("B")
        btn_c = QPushButton("C")
        btn_d = QPushButton("D")
        btn_e = QPushButton("E")
        btn_f = QPushButton("F")
        btn_g = QPushButton("G")
        btn_h = QPushButton("H")
        btn_i = QPushButton("I")
        btn_j = QPushButton("J")
        btn_k = QPushButton("K")
        btn_l = QPushButton("L")
        btn_m = QPushButton("M")
        btn_n = QPushButton("N")
        btn_o = QPushButton("O")
        btn_p = QPushButton("P")
        btn_q = QPushButton("Q")
        btn_r = QPushButton("R")
        btn_s = QPushButton("S")
        btn_t = QPushButton("T")
        btn_u = QPushButton("U")
        btn_v = QPushButton("V")
        btn_w = QPushButton("W")
        btn_x = QPushButton("X")
        btn_y = QPushButton("Y")
        btn_z = QPushButton("Z")

        btn_0 = QPushButton("0")
        btn_1 = QPushButton("1")
        btn_2 = QPushButton("2")
        btn_3 = QPushButton("3")
        btn_4 = QPushButton("4")
        btn_5 = QPushButton("5")
        btn_6 = QPushButton("6")
        btn_7 = QPushButton("7")
        btn_8 = QPushButton("8")
        btn_9 = QPushButton("9")

        btn_at = QPushButton("@")
        btn_comma = QPushButton(",")
        btn_period = QPushButton(".")
        btn_question_mark = QPushButton("?")
        btn_slash = QPushButton("/")

        self.option_letter_buttons = [btn_a, btn_b, btn_c, btn_d, btn_e,
                                      btn_f, btn_g, btn_h, btn_i, btn_j,
                                      btn_k, btn_l, btn_m, btn_n, btn_o,
                                      btn_p, btn_q, btn_r, btn_s, btn_t,
                                      btn_u, btn_v, btn_w, btn_x, btn_y,
                                      btn_z]

        self.option_number_buttons = [btn_0, btn_1, btn_2, btn_3, btn_4,
                                      btn_5, btn_6, btn_7, btn_8, btn_9]

        self.option_symbol_buttons = [btn_at, btn_comma, btn_period, btn_question_mark, btn_slash]

        total_num_option_buttons = len(self.option_letter_buttons) + len(self.option_number_buttons) + len(self.option_symbol_buttons)
        num_columns = 5
        num_rows = ceil(total_num_option_buttons / num_columns)
        self.all_buttons = self.option_letter_buttons + self.option_number_buttons + self.option_symbol_buttons

        grid_index = 0
        for col_idx in range(num_columns):
            for row_idx in range(num_rows):
                if grid_index >= len(self.all_buttons):
                    continue
                button = self.all_buttons[grid_index]
                button.setObjectName(str(grid_index))
                button.clicked.connect(self.on_choice_clicked)
                button.setEnabled(False)
                options_grid.addWidget(button, col_idx, row_idx)
                grid_index += 1


    def enable_relevant_buttons(self):
        for button in self.all_buttons:
            button.setEnabled(False)

        mode_combo_box_idx = self.included_items_combo_box.currentIndex()
        if mode_combo_box_idx == 0:  # letters only
            self.answer = random.choice(ascii_uppercase)
            for button in self.option_letter_buttons:
                button.setEnabled(True)
        elif mode_combo_box_idx == 1:  # numbers only
            self.answer = str(random.randint(0, 9))
            for button in self.option_number_buttons:
                button.setEnabled(True)
        elif mode_combo_box_idx == 2:  # symbols only
            self.answer = random.choice(self.symbol_list)
            for button in self.option_symbol_buttons:
                button.setEnabled(True)
        elif mode_combo_box_idx == 3:  # letters and numbers
            letters_and_numbers = self.option_letter_buttons + self.option_number_buttons
            random_int = random.randint(0, 9)
            random_letter = random.choice(ascii_uppercase)
            if random.randint(0, 1) == 0:
                self.answer = str(random_int)
            else:
                self.answer = random_letter
            for button in letters_and_numbers:
                button.setEnabled(True)
        elif mode_combo_box_idx == 4:  # all symbols
            random_int = random.randint(0, 9)
            random_letter = random.choice(ascii_uppercase)
            random_symbol = random.choice(self.symbol_list)
            rand_idx = random.randint(0, 2)
            if rand_idx == 0:
                self.answer = str(random_int)
            elif rand_idx == 1:
                self.answer = random_letter
            else:
                self.answer = random_symbol
            for button in self.all_buttons:
                button.setEnabled(True)


    def on_play_button_pressed(self):
        self.play_button.setEnabled(False)
        self.enable_relevant_buttons()

        print("ANSWER: " + self.answer)

        self.replay_button.setEnabled(True)

        if self.answer.upper() in ascii_uppercase:
            self.play_character_sound("assets/letter_morse_audio", self.answer + ".mp3")
        elif self.answer.isnumeric():
            self.play_character_sound("assets/number_morse_audio", self.answer + ".mp3")
        elif self.answer in self.symbol_list:
            symbol_file_name = None

            if self.answer == self.symbol_list[0]:
                symbol_file_name = "@"
            elif self.answer == self.symbol_list[1]:
                symbol_file_name = "comma"
            elif self.answer == self.symbol_list[2]:
                symbol_file_name = "period"
            elif self.answer == self.symbol_list[3]:
                symbol_file_name = "questionmark"
            elif self.answer == self.symbol_list[4]:
                symbol_file_name = "slash"

            self.play_character_sound("assets/symbol_morse_audio", symbol_file_name + ".mp3")


    def on_replay_button_pressed(self):
        print("replay button pressed")
        self.audioplayer.play(loop=False, block=True)


    # def on_audio_state_changed(self, status):
    #     if status == QMediaPlayer.MediaStatus.EndOfMedia:
    #         self.play_button.setEnabled(True)


    def play_character_sound(self, directory, character):
        file_path = path.join(directory, character.lower())
        self.play_audio(file_path)


    def on_choice_clicked(self):
        choice_index = self.sender().objectName()
        choice = self.all_buttons[int(choice_index)].text()

        if choice == self.answer:
            self.on_correct()
        else:
            self.on_wrong()

        for button in self.all_buttons:
            button.setEnabled(False)

        self.replay_button.setEnabled(False)


    def on_wrong(self):
        self.play_audio("assets/wrong.wav", 200)
        self.num_wrong += 1
        self.num_wrong_text.setText("Wrong: " + str(self.num_wrong))
        self.play_button.setEnabled(True)


    def on_correct(self):
        self.play_audio("assets/correct.wav", 150)
        self.num_correct += 1
        self.num_correct_text.setText("Correct: " + str(self.num_correct))
        self.play_button.setEnabled(True)


    def play_audio(self, file_path, volume=50):
        self.audioplayer = AudioPlayer(file_path)
        self.audioplayer.play(loop=False, block=True)
        self.audioplayer.volume = volume
        # if self.media_player:
        #     self.media_player.stop()
        #
        # self.media_player = QMediaPlayer()
        # self.media_player.mediaStatusChanged.connect(self.on_audio_state_changed)
        # self.audio_output = QAudioOutput()
        # self.media_player.setAudioOutput(self.audio_output)
        # self.media_player.setSource(QUrl.fromLocalFile(file_path))
        # self.audio_output.setVolume(volume)
        #
        # speed_option = self.speed_combo_box.currentIndex()
        # if speed_option == 0:
        #     self.media_player.setPlaybackRate(0.25)
        # elif speed_option == 1:
        #     self.media_player.setPlaybackRate(.50)
        # elif speed_option == 2:
        #     self.media_player.setPlaybackRate(.75)
        # else:
        #     self.media_player.setPlaybackRate(1)
        #
        # self.media_player.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    apply_stylesheet(app, theme="dark_cyan.xml")
    window.setStyleSheet("QLabel { font-size: 15px; text-transform: uppercase; }")
    window.show()
    app.exec()