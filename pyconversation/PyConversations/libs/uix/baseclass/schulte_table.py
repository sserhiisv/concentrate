import string

from kivy.uix.screenmanager import Screen


class SchulteTable(Screen):
    def __init__(self, **kwargs):
        super(SchulteTable, self).__init__(**kwargs)
        self.pressed_number = 0
        self.pressed_letter_index = -1

        self.max_value = 25
        self.finished = False
        self.letters = list(string.ascii_lowercase)[:25]

    def check_numbers(self, value):
        if int(value) == self.pressed_number + 1:
            self.pressed_number += 1
            self.ids['label'].text = f"Next: {str(self.pressed_number + 1)}"

            if self.pressed_number == self.max_value:
                self.finished = True
                self.pressed_number = 0
            else:
                self.finished = False

    def check_letters(self, value):
        if self.letters.index(value.lower()) == self.pressed_letter_index + 1:
            self.pressed_letter_index += 1
            next_value = self.letters[self.letters.index(value.lower()) + 1]
            self.ids['label'].text = f"Next: {next_value}"

            if self.pressed_letter_index + 1 == self.max_value:
                self.finished = True
                self.pressed_letter_index = -1
            else:
                self.finished = False

    def submit(self, value, button_id):
        if not value.isnumeric():
            self.check_letters(value)
        elif value.isnumeric():
            self.check_numbers(value)
