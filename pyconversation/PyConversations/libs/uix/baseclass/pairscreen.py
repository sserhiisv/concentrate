from kivy.uix.screenmanager import Screen


class Pair(Screen):
    def __init__(self, **kwargs):
        super(Pair, self).__init__(**kwargs)
        self.win_count = 5
        self.attempts = 0
        self.won_count = 0

        self.pressed = None
        self.pressed_button_id = None

        self.check = False
        self.finish = False

        self.result = {}

    def say_hello(self, text, button_id):
        self.ids[button_id].background_color = [255/255, 214/255, 153/255, 1]
        # self.ids[button_id].color = [1, 1, 1, 1]
        if self.attempts == 0:
            self.result = {}

        if not self.pressed:
            self.pressed = text
            self.pressed_button_id = button_id
            self.check = False
        else:
            if self.pressed_button_id == button_id:
                self.pressed = None
                self.pressed_button_id = None
                self.ids[button_id].background_color = [255 / 255, 235 / 255, 204 / 255, 1]
            else:
                self.attempts += 1
                if self.pressed == text:
                    self.won_count += 1
                    if self.won_count == self.win_count:
                        self.finish = True
                    else:
                        self.pressed = None
                else:
                    self.pressed = None
                self.check = True

        self.result = {
            'check': self.check,
            'finish': self.finish,
            'attempts': self.attempts,
            'won_count': self.won_count,
            'win_count': self.win_count
        }

        if self.attempts == self.win_count or self.finish:
            self.pressed = None
            self.check = False
            self.finish = False
            self.attempts = 0
            self.won_count = 0
