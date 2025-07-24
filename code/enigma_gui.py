import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QPushButton, QLabel, 
                             QComboBox, QGroupBox)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QTimer

from enigma_logic import Enigma

class EnigmaPyQtGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.enigma_engine = Enigma()
        self.is_locked = False
        self.plugboard_first_letter = None
        self.plugboard_pairs = {}
        self.input_text = ""
        self.output_text = ""
        self.undo_stack = []
        self.redo_stack = []

        self.setWindowTitle("Enigma Machine - Bismarck")
        self.setStyleSheet("background-color: #3C3F41; color: #F2F2F2;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        settings_panel = self._create_settings_panel()
        lampboard = self._create_lampboard()
        keyboard = self._create_keyboard()
        io_display = self._create_io_display()

        main_layout.addWidget(settings_panel)
        main_layout.addWidget(lampboard)
        main_layout.addWidget(keyboard)
        main_layout.addWidget(io_display)
        main_layout.addStretch()

    def _create_settings_panel(self):
        group_box = QGroupBox("Machine Configuration")
        group_box.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        main_layout = QHBoxLayout()

        rotor_reflector_layout = QVBoxLayout()
        rotor_box = QGroupBox("Rotors & Reflector")
        rotor_box.setFont(QFont("Segoe UI", 10))
        rotor_layout = QHBoxLayout()

        self.rotor_vars = []
        self.pos_labels = []
        rotor_options = [str(i) for i in range(1, 9)]

        for i, label in enumerate(["Left", "Middle", "Right"]):
            rotor_col = QVBoxLayout()
            rotor_col.addWidget(QLabel(label))

            combo = QComboBox()
            combo.addItems(rotor_options)
            combo.setCurrentText(str(3-i))
            self.rotor_vars.append(combo)
            rotor_col.addWidget(combo)

            pos_label = QLabel("A")
            pos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pos_label.setStyleSheet("background-color: black; color: white; border: 1px solid #777; padding: 5px;")
            pos_label.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
            self.pos_labels.append(pos_label)
            rotor_col.addWidget(pos_label)

            up_btn = QPushButton("\u25B2")
            down_btn = QPushButton("\u25BC")
            up_btn.clicked.connect(lambda _, i=i: self._change_pos(i, 1))
            down_btn.clicked.connect(lambda _, i=i: self._change_pos(i, -1))
            rotor_col.addWidget(up_btn)
            rotor_col.addWidget(down_btn)
            rotor_layout.addLayout(rotor_col)

        reflector_col = QVBoxLayout()
        reflector_col.addWidget(QLabel("Reflector"))
        self.reflector_var = QComboBox()
        self.reflector_var.addItems(["B", "C"])
        reflector_col.addWidget(self.reflector_var)
        reflector_col.addStretch()
        rotor_layout.addLayout(reflector_col)
        rotor_box.setLayout(rotor_layout)
        rotor_reflector_layout.addWidget(rotor_box)

        self.lock_button = QPushButton("Lock Settings")
        self.lock_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.lock_button.setStyleSheet("background-color: #50A14F; color: white; padding: 10px;")
        self.lock_button.clicked.connect(self._toggle_lock)
        rotor_reflector_layout.addWidget(self.lock_button)
        rotor_reflector_layout.addStretch()

        plugboard_box = QGroupBox("Plugboard (Steckerbrett)")
        plugboard_box.setFont(QFont("Segoe UI", 10))
        plug_layout = QVBoxLayout()
        key_layout = QGridLayout()

        self.plug_buttons = {}
        keyboard_layout = "QWERTZUIOPASDFGHJKLYXCVBNM"
        for i, char in enumerate(keyboard_layout):
            row, col = divmod(i, 10) if i < 20 else (2, i-18)
            btn = QPushButton(char)
            btn.setFixedSize(40, 40)
            btn.clicked.connect(lambda _, c=char: self._plug_press(c))
            key_layout.addWidget(btn, row, col)
            self.plug_buttons[char] = btn

        self.plug_display = QLabel("Pairs: ")
        self.plug_display.setFont(QFont("Courier New", 10))

        plug_layout.addLayout(key_layout)
        plug_layout.addWidget(self.plug_display)
        plugboard_box.setLayout(plug_layout)

        main_layout.addLayout(rotor_reflector_layout)
        main_layout.addWidget(plugboard_box)
        group_box.setLayout(main_layout)
        return group_box

    def _create_lampboard(self):
        group_box = QGroupBox("Lampboard")
        group_box.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        grid_layout = QGridLayout()
        self.lamps = {}
        keyboard_layout = "QWERTZUIOPASDFGHJKLYXCVBNM"
        for i, char in enumerate(keyboard_layout):
            row, col = divmod(i, 10) if i < 20 else (2, i-18)
            lamp = QLabel(char)
            lamp.setFixedSize(60, 60)
            lamp.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lamp.setFont(QFont("Courier New", 20, QFont.Weight.Bold))
            lamp.setStyleSheet("background-color: #2B2B2B; color: #555; border-radius: 30px; border: 2px solid #1E1E1E;")
            grid_layout.addWidget(lamp, row, col)
            self.lamps[char] = lamp
        group_box.setLayout(grid_layout)
        return group_box

    def _create_keyboard(self):
        group_box = QGroupBox("Keyboard")
        group_box.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        grid_layout = QGridLayout()
        keyboard_layout = "QWERTZUIOPASDFGHJKLYXCVBNM"
        for i, char in enumerate(keyboard_layout):
            row, col = divmod(i, 10) if i < 20 else (2, i-18)
            btn = QPushButton(char)
            btn.setFixedSize(60, 60)
            btn.setFont(QFont("Courier New", 16, QFont.Weight.Bold))
            btn.clicked.connect(lambda _, c=char: self._key_press(c))
            grid_layout.addWidget(btn, row, col)
        group_box.setLayout(grid_layout)
        return group_box

    def _create_io_display(self):
        group_box = QGroupBox("Session Log")
        layout = QHBoxLayout()
        font = QFont("Courier New", 14)
        self.input_display_label = QLabel("Input: ")
        self.input_display_label.setFont(font)
        self.output_display_label = QLabel("Output: ")
        self.output_display_label.setFont(font)

        undo_btn = QPushButton("Undo")
        undo_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        undo_btn.clicked.connect(self.undo)

        redo_btn = QPushButton("Redo")
        redo_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        redo_btn.clicked.connect(self.redo)

        layout.addWidget(self.input_display_label)
        layout.addWidget(self.output_display_label)
        layout.addWidget(undo_btn)
        layout.addWidget(redo_btn)

        group_box.setLayout(layout)
        return group_box

    def _update_rotor_display(self, rotor_index, new_val):
        self.pos_labels[rotor_index].setText(chr(ord('A') + new_val))

    def _change_pos(self, rotor_index, direction):
        if self.is_locked: return
        label = self.pos_labels[rotor_index]
        current_char = label.text()
        current_val = ord(current_char) - ord('A')
        new_val = (current_val + direction) % 26
        self._update_rotor_display(rotor_index, new_val)

    def _plug_press(self, letter):
        if self.is_locked: return
        if not self.plugboard_first_letter:
            self.plugboard_first_letter = letter
            self.plug_buttons[letter].setStyleSheet("background-color: #FFA500;")
        else:
            if self.plugboard_first_letter != letter:
                pair = tuple(sorted((self.plugboard_first_letter, letter)))
                self.plugboard_pairs[pair[0]] = pair[1]

                self.plug_buttons[self.plugboard_first_letter].setEnabled(False)
                self.plug_buttons[letter].setEnabled(False)
                self.plug_buttons[self.plugboard_first_letter].setStyleSheet("")
                self.plug_buttons[letter].setStyleSheet("")
                self.plugboard_first_letter = None

                pairs_str = " ".join([f"{k}{v}" for k, v in self.plugboard_pairs.items()])
                self.plug_display.setText(f"Pairs: {pairs_str}")
            else:
                self.plug_buttons[letter].setStyleSheet("")
                self.plugboard_first_letter = None

    def _toggle_lock(self):
        self.is_locked = not self.is_locked
        if self.is_locked:
            try:
                rotors = [int(combo.currentText()) for combo in self.rotor_vars]
                positions = [ord(label.text()) - ord('A') + 1 for label in self.pos_labels]
                reflector = self.reflector_var.currentText()
                plug_str = " ".join([f"{k}{v}" for k,v in self.plugboard_pairs.items()])

                self.enigma_engine.set_rotors(rotors)
                self.enigma_engine.set_reflector(reflector)
                self.enigma_engine.set_rotor_positions(positions)
                self.enigma_engine.set_plugboard(plug_str)

                self.lock_button.setText("Unlock Machine")
                self.lock_button.setStyleSheet("background-color: #D34C4C;")
                self.input_text = ""
                self.output_text = ""
                self.undo_stack.clear()
                self.redo_stack.clear()
                self._update_io_display()

            except ValueError as e:
                print(f"Error: {e}")
                self.is_locked = False
        else:
            self.lock_button.setText("Lock Settings")
            self.lock_button.setStyleSheet("background-color: #50A14F;")
            for btn in self.plug_buttons.values():
                btn.setEnabled(True)
                btn.setStyleSheet("")
            self.plugboard_pairs.clear()
            self.plug_display.setText("Pairs: ")
            self.plugboard_first_letter = None

    def _key_press(self, letter):
        if not self.is_locked: return

        # Save current state to undo stack
        state = {
            'input': self.input_text,
            'output': self.output_text,
            'rotors': [self.enigma_engine.left_pos,
                       self.enigma_engine.middle_pos,
                       self.enigma_engine.right_pos]
        }
        self.undo_stack.append(state)
        self.redo_stack.clear()

        self.input_text += letter
        encrypted_char = self.enigma_engine.process_string(letter)
        self.output_text += encrypted_char
        self._update_io_display()

        rotor_state = [self.enigma_engine.left_pos, self.enigma_engine.middle_pos, self.enigma_engine.right_pos]
        for i, pos in enumerate(rotor_state):
            self._update_rotor_display(i, pos)

        self._light_lamp(encrypted_char)

    def undo(self):
        if not self.undo_stack: return
        state = {
            'input': self.input_text,
            'output': self.output_text,
            'rotors': [self.enigma_engine.left_pos,
                       self.enigma_engine.middle_pos,
                       self.enigma_engine.right_pos]
        }
        self.redo_stack.append(state)
        prev_state = self.undo_stack.pop()
        self.input_text = prev_state['input']
        self.output_text = prev_state['output']
        self.enigma_engine.left_pos, self.enigma_engine.middle_pos, self.enigma_engine.right_pos = prev_state['rotors']

        for i, pos in enumerate(prev_state['rotors']):
            self._update_rotor_display(i, pos)

        self._update_io_display()

    def redo(self):
        if not self.redo_stack: return
        state = {
            'input': self.input_text,
            'output': self.output_text,
            'rotors': [self.enigma_engine.left_pos,
                       self.enigma_engine.middle_pos,
                       self.enigma_engine.right_pos]
        }
        self.undo_stack.append(state)
        next_state = self.redo_stack.pop()
        self.input_text = next_state['input']
        self.output_text = next_state['output']
        self.enigma_engine.left_pos, self.enigma_engine.middle_pos, self.enigma_engine.right_pos = next_state['rotors']

        for i, pos in enumerate(next_state['rotors']):
            self._update_rotor_display(i, pos)

        self._update_io_display()

    def _light_lamp(self, letter):
        for lamp in self.lamps.values():
            lamp.setStyleSheet("background-color: #2B2B2B; color: #555; border-radius: 30px; border: 2px solid #1E1E1E;")

        if letter in self.lamps:
            lamp = self.lamps[letter]
            lamp.setStyleSheet("background-color: #FFFF00; color: #000; border-radius: 30px; border: 2px solid #AAA;")
            QTimer.singleShot(500, lambda: lamp.setStyleSheet("background-color: #2B2B2B; color: #555; border-radius: 30px; border: 2px solid #1E1E1E;"))

    def _update_io_display(self):
        self.input_display_label.setText(f"Input: {self.input_text}")
        self.output_display_label.setText(f"Output: {self.output_text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnigmaPyQtGUI()
    window.show()
    sys.exit(app.exec())
