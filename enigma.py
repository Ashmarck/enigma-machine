class Enigma:
    def __init__(self):
        self.reducing_list = [chr(i) for i in range(65, 91)]
        self.plugboard = [chr(i) for i in range(65, 91)]
        self.connection_count = 0

        self.main_rotor = [chr(i) for i in range(65, 91)]
        self.rotor_dict = {
            1: ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q'),
            2: ("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E'),
            3: ("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V'),
            4: ("ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J'),
            5: ("VZBRGITYUPSDNHLXAWMJQOFECK", 'Z'),
            6: ("JPGVOUMFYQBENHZRDKASXLICTW", 'M'),
            7: ("NZJHGRCXMYSWBOUFAIVLPEKQDT", 'M'),
            8: ("FKQHTLXOCBJSPDZRAMEWNIUYGV", 'M')
        }
        self.reflector_dict = {
            1: "EJMZALYXVBWFCRQUONTSPIKHGD",
            2: "YRUHQSLDPXNGOKMIEBFZCWVJAT",
            3: "FVPJIAOYEDRZXWGCTKUQSBNMHL"
        }

    def setupConnection(self, alpha1, alpha2):
        if self.connection_count >= 10:
            print("ATMOST 10 CONNECTIONS CAN BE MADE.")
            return
        if alpha1 not in self.plugboard or alpha2 not in self.plugboard:
            print(f"Invalid connection characters: {alpha1}, {alpha2}")
            return

        self.reducing_list.remove(alpha1)
        self.reducing_list.remove(alpha2)
        alpha1_index = self.plugboard.index(alpha1)
        alpha2_index = self.plugboard.index(alpha2)
        self.plugboard[alpha1_index] = alpha2
        self.plugboard[alpha2_index] = alpha1
        self.connection_count += 1

    def selectRotor(self, rotors):
        while True:
            if len(set(rotors)) != 3 or max(rotors) > 8 or min(rotors) < 1:
                print("ONLY 3 UNIQUE ROTORS BETWEEN 1 AND 8 ARE ALLOWED.")
                rotors = self.promptRotorSelection()
            else:
                self.right_rotor, self.right_notch = self.rotor_dict.get(rotors[0])
                self.middle_rotor, self.middle_notch = self.rotor_dict.get(rotors[1])
                self.left_rotor, self.left_notch = self.rotor_dict.get(rotors[2])
                self.right_rotor = list(self.right_rotor)
                self.middle_rotor = list(self.middle_rotor)
                self.left_rotor = list(self.left_rotor)
                break

    def selectReflector(self, reflector):
        if reflector > 3 or reflector < 1:
            print("THERE ARE ONLY 3 REFLECTORS AVAILABLE TO CHOOSE FROM.")
            reflector = self.promptReflectorSelection()
        else:
            self.reflector = self.reflector_dict.get(reflector)

    def instructions(self):
        for i in range(1, 9):
            rotor, notch = self.rotor_dict.get(i)
            print(f"{i} ROTOR: {rotor} (Notch: {notch})")
        print()
        for i in range(1, 4):
            print(f"{i} REFLECTOR: {self.reflector_dict.get(i)}")

    def rotateRotor(self, rotor):
        return rotor[-1:] + rotor[:-1]

    def encodeRotor(self, notations):
        right_rotor_set = [self.main_rotor, self.right_rotor]
        middle_rotor_set = [self.main_rotor, self.middle_rotor]
        left_rotor_set = [self.main_rotor, self.left_rotor]

        rotor1_count, rotor2_count, rotor3_count = 0, 0, 0

        if 0 in notations:
            print("ENTER NOTATIONS FROM 1 TO 26.")
            notations = self.promptNotationSelection()
        else:
            for i in range(notations[0] - 1):
                right_rotor_set[0] = self.rotateRotor(right_rotor_set[0])
                right_rotor_set[1] = self.rotateRotor(right_rotor_set[1])

            for i in range(notations[1] - 1):
                middle_rotor_set[0] = self.rotateRotor(middle_rotor_set[0])
                middle_rotor_set[1] = self.rotateRotor(middle_rotor_set[1])

            for i in range(notations[2] - 1):
                left_rotor_set[0] = self.rotateRotor(left_rotor_set[0])
                left_rotor_set[1] = self.rotateRotor(left_rotor_set[1])

        while True:
            string = input("ENTER A STRING: ").upper()
            if string == "QUIT":
                break
            letter_list = list(string)
            encoded_list = []

            special_chars = [chr(i) for i in range(32, 48)] + [chr(i) for i in range(58, 65)] + \
                            [chr(i) for i in range(91, 97)] + [chr(i) for i in range(123, 127)]

            for letter in letter_list:
                if letter in special_chars:
                    encoded_list.append(letter)
                else:
                    plugboard_letter = letter
                    plugboard_letter_index = self.plugboard.index(plugboard_letter)

                    right_rotor_letter = right_rotor_set[1][plugboard_letter_index]
                    right_rotor_index = right_rotor_set[0].index(right_rotor_letter)

                    middle_rotor_letter = middle_rotor_set[1][right_rotor_index]
                    middle_rotor_index = middle_rotor_set[0].index(middle_rotor_letter)

                    left_rotor_letter = left_rotor_set[1][middle_rotor_index]
                    left_rotor_index = left_rotor_set[0].index(left_rotor_letter)

                    in_reflector_letter = self.reflector[left_rotor_index]
                    out_reflector_index = self.main_rotor.index(in_reflector_letter)

                    reverse_left_rotor_letter = left_rotor_set[0][out_reflector_index]
                    reverse_left_rotor_index = left_rotor_set[1].index(reverse_left_rotor_letter)

                    reverse_middle_rotor_letter = middle_rotor_set[0][reverse_left_rotor_index]
                    reverse_middle_rotor_index = middle_rotor_set[1].index(reverse_middle_rotor_letter)

                    reverse_right_rotor_letter = right_rotor_set[0][reverse_middle_rotor_index]
                    reverse_right_rotor_index = right_rotor_set[1].index(reverse_right_rotor_letter)

                    reverse_plugboard_letter = self.plugboard[reverse_right_rotor_index]
                    reverse_letter_index = self.main_rotor.index(reverse_plugboard_letter)
                    reverse_letter = self.main_rotor[reverse_letter_index]

                    encoded_list.append(reverse_letter)

                    right_rotor_set[0] = self.rotateRotor(right_rotor_set[0])
                    right_rotor_set[1] = self.rotateRotor(right_rotor_set[1])
                    rotor1_count += 1

                    if rotor1_count % 26 == 0 or self.main_rotor[0] == self.right_notch:
                        middle_rotor_set[0] = self.rotateRotor(middle_rotor_set[0])
                        middle_rotor_set[1] = self.rotateRotor(middle_rotor_set[1])
                        rotor1_count = 0
                        rotor2_count += 1

                    if rotor2_count % 26 == 0 or self.main_rotor[0] == self.middle_notch:
                        left_rotor_set[0] = self.rotateRotor(left_rotor_set[0])
                        left_rotor_set[1] = self.rotateRotor(left_rotor_set[1])
                        rotor2_count = 0
                        rotor3_count += 1

            print(f"ENCODED STRING: {''.join(encoded_list)}")

    def promptRotorSelection(self):
        while True:
            try:
                rotor1 = int(input("CHOOSE RIGHT ROTOR (1-8): "))
                rotor2 = int(input("CHOOSE MIDDLE ROTOR (1-8): "))
                rotor3 = int(input("CHOOSE LEFT ROTOR (1-8): "))
                return [rotor1, rotor2, rotor3]
            except ValueError:
                print("INVALID INPUT. PLEASE ENTER NUMBERS BETWEEN 1 AND 8.")
                
    def promptReflectorSelection(self):
        while True:
            try:
                reflector = int(input("CHOOSE REFLECTOR (1-3): "))
                return reflector
            except ValueError:
                print("INVALID INPUT. PLEASE ENTER A NUMBER BETWEEN 1 AND 3.")
                
    def promptNotationSelection(self):
        while True:
            try:
                notation1 = int(input("CHOOSE NOTATION (RIGHT ROTOR 1-26): "))
                notation2 = int(input("CHOOSE NOTATION (MIDDLE ROTOR 1-26): "))
                notation3 = int(input("CHOOSE NOTATION (LEFT ROTOR 1-26): "))
                return [notation1, notation2, notation3]
            except ValueError:
                print("INVALID INPUT. PLEASE ENTER NUMBERS BETWEEN 1 AND 26.")

if __name__ == "__main__":
    enigma = Enigma()
    enigma.setupConnection('A', 'R')
    enigma.setupConnection('H', 'D')
    enigma.setupConnection('C', 'L')
    enigma.setupConnection('P', 'E')
    enigma.setupConnection('V', 'F')
    enigma.setupConnection('X', 'O')
    enigma.setupConnection('I', 'Z')
    enigma.setupConnection('S', 'G')
    enigma.setupConnection('J', 'T')
    enigma.setupConnection('B', 'M')
    enigma.instructions()
    print()

    enigma.selectRotor(enigma.promptRotorSelection())
    enigma.selectReflector(enigma.promptReflectorSelection())
    enigma.encodeRotor(enigma.promptNotationSelection())
