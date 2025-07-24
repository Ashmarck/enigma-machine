class Enigma:
    def __init__(self):
        
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
       
        self.rotor_dict = {
            1: ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q'), 2: ("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E'),
            3: ("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V'), 4: ("ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J'),
            5: ("VZBRGITYUPSDNHLXAWMJQOFECK", 'Z'), 6: ("JPGVOUMFYQBENHZRDKASXLICTW", 'M'),
            7: ("NZJHGRCXMYSWBOUFAIVLPEKQDT", 'M'), 8: ("FKQHTLXOCBJSPDZRAMEWNIUYGV", 'M')
        }
        self.reflector_dict = {
            'B': "YRUHQSLDPXNGOKMIEBFZCWVJAT",
            'C': "FVPJIAOYEDRZXWGCTKUQSBNMHL"
        }
        self.reset_machine_state()

    def reset_machine_state(self):
        self.plugboard = {char: char for char in self.alphabet}
        self.right_rotor, self.middle_rotor, self.left_rotor = None, None, None
        self.right_notch, self.middle_notch, self.left_notch = None, None, None
        self.reflector = None
        self.right_pos, self.middle_pos, self.left_pos = 0, 0, 0

    def set_plugboard(self, pairs):
        self.plugboard = {char: char for char in self.alphabet}
        if not pairs:
            return
        
        used_chars = set()
        for pair in pairs.upper().split():
            if len(pair) != 2 or not pair.isalpha():
                raise ValueError(f"Invalid plugboard pair: '{pair}'. Pairs must be two letters.")
            p1, p2 = pair[0], pair[1]
            if p1 in used_chars or p2 in used_chars:
                raise ValueError(f"Letter used in more than one plugboard pair: '{pair}'.")

            self.plugboard[p1] = p2
            self.plugboard[p2] = p1
            used_chars.add(p1)
            used_chars.add(p2)

    def set_rotors(self, rotor_choices):
        if len(set(rotor_choices)) != 3:
            raise ValueError("Rotor choices must be unique.")
        
        self.right_rotor_wiring, self.right_notch = self.rotor_dict[rotor_choices[0]]
        self.middle_rotor_wiring, self.middle_notch = self.rotor_dict[rotor_choices[1]]
        self.left_rotor_wiring, self.left_notch = self.rotor_dict[rotor_choices[2]]
    
    def set_reflector(self, reflector_choice):
        if reflector_choice not in self.reflector_dict:
            raise ValueError("Invalid reflector choice.")
        self.reflector = self.reflector_dict[reflector_choice]

    def set_rotor_positions(self, positions):
        self.right_pos = positions[0] - 1
        self.middle_pos = positions[1] - 1
        self.left_pos = positions[2] - 1
        
    def _rotate(self):
        middle_turnover = self.alphabet[self.middle_pos] == self.middle_notch
        right_turnover = self.alphabet[self.right_pos] == self.right_notch

        if middle_turnover:
            self.middle_pos = (self.middle_pos + 1) % 26
            self.left_pos = (self.left_pos + 1) % 26
        
        if right_turnover:
            self.middle_pos = (self.middle_pos + 1) % 26

        self.right_pos = (self.right_pos + 1) % 26

    def _pass_through(self, char_code, wiring, pos):
        entry_code = (char_code + pos) % 26
        exit_char = wiring[entry_code]
        exit_code = (self.alphabet.index(exit_char) - pos + 26) % 26
        return exit_code

    def _pass_through_inverse(self, char_code, wiring, pos):
        entry_code = (char_code + pos) % 26
        entry_char = self.alphabet[entry_code]
        exit_code = (wiring.index(entry_char) - pos + 26) % 26
        return exit_code

    def process_string(self, text):
        processed_text = ""
        for char in text.upper():
            if char in self.alphabet:
                processed_text += self._process_char(char)
            else:
                processed_text += char
        return processed_text

    def _process_char(self, char):
        self._rotate()

        # Path from input to reflector
        char = self.plugboard[char]
        char_code = self.alphabet.index(char)
        
        # Through rotors right-to-left
        code_after_r = self._pass_through(char_code, self.right_rotor_wiring, self.right_pos)
        code_after_m = self._pass_through(code_after_r, self.middle_rotor_wiring, self.middle_pos)
        code_after_l = self._pass_through(code_after_m, self.left_rotor_wiring, self.left_pos)
        
        # Reflector
        reflected_char = self.reflector[code_after_l]
        reflected_code = self.alphabet.index(reflected_char)
        
        # Path from reflector back to output
        code_after_l_inv = self._pass_through_inverse(reflected_code, self.left_rotor_wiring, self.left_pos)
        code_after_m_inv = self._pass_through_inverse(code_after_l_inv, self.middle_rotor_wiring, self.middle_pos)
        code_after_r_inv = self._pass_through_inverse(code_after_m_inv, self.right_rotor_wiring, self.right_pos)
        
        output_char = self.alphabet[code_after_r_inv]
        output_char = self.plugboard[output_char]
        
        return output_char