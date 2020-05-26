import random
import string
import time

from datetime import datetime
from collections import OrderedDict

from kivy.storage.jsonstore import JsonStore


class SchulteTableCore:

    def __init__(self, base, version):
        self.base = base
        self.start_time = None
        self.values = None

        self.button_color = [54 / 255, 48 / 255, 115 / 255, 1]
        self.background_color = [255 / 255, 235 / 255, 204 / 255, 1]

        self.stored_data = JsonStore('data/results/data.json')

        self.version = version

        self.NUMBERS = 0
        self.LETTERS = 1
        self.versions = {
            'numbers': self.NUMBERS,
            'letters': self.LETTERS
        }

        self.current_version = self.NUMBERS

        self.DYNAMIC = 0
        self.STATIC = 1
        self.modes = {
            'dynamic': self.DYNAMIC,
            'static': self.STATIC
        }
        self.current_mode = self.DYNAMIC

        self.LOWER = 0
        self.UPPER = 1
        self.MIXED = 2
        self.cases = {
            'lower': self.LOWER,
            'upper': self.UPPER,
            'mixed': self.MIXED
        }
        self.current_case = self.LOWER

        self.colored = False

        self.colors = (
            [17/255, 46/255, 81/255, 1],
            [205/255, 32/255, 38/255, 1],
            [46/255, 133/255, 64/255, 1],
            [92/255, 42/255, 125/255, 1],
            [232/255, 123/255, 14/255, 1]
        )

    def show_end_schulte_game(self, finished):
        if finished:
            self.base.nav_drawer.set_state('close')

            total_time = datetime.now() - self.start_time
            total_time_str = f'{(total_time.seconds % 3600) // 60}:{total_time.seconds % 60}'

            self.stored_data.put(
                int(time.time()),
                version=self.version,
                case=self.current_case,
                mode=self.current_mode,
                time=total_time_str
            )

            data = list(OrderedDict(self.stored_data))

            if len(data) > 5:
                data = data[:5]

            for el in data:
                x = self.stored_data.get(el)
                case = list(self.cases.keys())[list(self.cases.values()).index(x.get("case"))]
                mode = list(self.modes.keys())[list(self.modes.values()).index(x.get("mode"))]

                ids = self.base.screen.ids.tryagain.ids
                label = getattr(ids, f'result_{str(data.index(el)+1)}')
                label.text = f'{x.get("version")}/{case}/{mode} - {x.get("time")}'


            self.base.screen.ids.tryagain.ids.label_result.text = total_time_str
            self.base.screen.ids.schulte_table.ids.label.text = ""

            button = self.base.screen.ids.tryagain.ids.start
            button.on_press = self.run
            self.base.manager.current = 'tryagain'
        else:
            self.run()

    def fill_in_table(self, values):
        for el in range(1, 26):
            pair_ids = self.base.screen.ids.schulte_table.ids
            source = f'button_{str(el)}'
            button = getattr(pair_ids, source)
            button.text = str(values[el - 1])
            button.background_normal = ''
            if self.colored:
                button.background_color = random.choice(self.colors)
                button.color = [250/255, 247/255, 245/255, 1]
            else:
                button.background_color = [255 / 255, 235 / 255, 204 / 255, 1]
                button.color = [0, 0, 0, 1]

    def generate_data(self):
        if self.versions[self.version] == self.NUMBERS:
            lower = self.base.screen.ids.schulte_table.ids.button_lower
            lower.text = ''
            upper = self.base.screen.ids.schulte_table.ids.button_upper
            upper.text = ''
            mixed = self.base.screen.ids.schulte_table.ids.button_mixed
            mixed.text = ''

            lower = self.base.screen.ids.schulte_table.ids.button_lower
            lower.background_color = [255 / 255, 235 / 255, 204 / 255, 1]
            lower.color = [1, 1, 1, 1]
            upper = self.base.screen.ids.schulte_table.ids.button_upper
            upper.background_color = [255 / 255, 235 / 255, 204 / 255, 1]
            upper.color = [1, 1, 1, 1]
            mixed = self.base.screen.ids.schulte_table.ids.button_mixed
            mixed.background_color = [255 / 255, 235 / 255, 204 / 255, 1]
            mixed.color = [1, 1, 1, 1]

            values = [el for el in range(1, 26)]
        elif self.versions[self.version] == self.LETTERS:

            for case, value in self.cases.items():
                ids = self.base.screen.ids.schulte_table.ids
                button = getattr(ids, f'button_{case}')
                button.text = case[0].upper() + case[1:]
                if self.current_case == value:
                    button.background_color = self.button_color
                    button.color = [1, 1, 1, 1]
                else:
                    button.background_color = self.background_color
                    button.color = [0, 0, 0, 1]

            if self.current_case == self.LOWER:
                values = list(string.ascii_lowercase)[:25]
            elif self.current_case == self.UPPER:
                values = list(string.ascii_uppercase)[:25]
            elif self.current_case == self.MIXED:
                upper_case = random.sample(list(string.ascii_uppercase)[:25], 12)
                lower_case = [
                    el for el in list(string.ascii_lowercase)[:25]
                    if el.upper() not in upper_case
                ]
                values = upper_case + lower_case
        return values

    def create_table(self):
        if self.current_mode == self.DYNAMIC:
            values = self.generate_data()
            random.shuffle(values)
            self.fill_in_table(values)
        elif self.current_mode == self.STATIC:
            if not self.values:
                values = self.generate_data()
                random.shuffle(values)
                self.values = values
            self.fill_in_table(self.values)

    def change_version(self, to_version, rerun=False):
        self.current_version = self.versions[to_version]
        if rerun:
            self.values = None
            self.run()

    def colorize(self, is_colorize, rerun=False):
        ids = self.base.screen.ids.schulte_table.ids
        curr_case = 'color' if self.colored else 'bw'
        button = getattr(ids, f'button_{curr_case}')
        button.background_color = [255 / 255, 235 / 255, 204 / 255, 1]
        button.color = [0, 0, 0, 1]

        self.colored = is_colorize
        new = 'color' if self.colored else 'bw'
        button = getattr(ids, f'button_{new}')
        button.background_color = [54 / 255, 48 / 255, 115 / 255, 1]
        button.color = [1, 1, 1, 1]

        if rerun:
            self.values = None
            self.run()

    def change_case(self, to_case, rerun=False):
        ids = self.base.screen.ids.schulte_table.ids

        curr_case = list(self.cases.keys())[list(self.cases.values()).index(self.current_case)]
        button = getattr(ids, f'button_{curr_case}')
        button.background_color = [255 / 255, 235 / 255, 204 / 255, 1]
        button.color = [0, 0, 0, 1]

        self.current_case = self.cases[to_case]
        button = getattr(ids, f'button_{to_case}')
        button.background_color = [54 / 255, 48 / 255, 115 / 255, 1]
        button.color = [1, 1, 1, 1]

        if rerun:
            self.values = None
            self.run()

    def change_mode(self, to_mode, rerun=False):
        ids = self.base.screen.ids.schulte_table.ids

        curr_mode = list(self.modes.keys())[list(self.modes.values()).index(self.current_mode)]
        button = getattr(ids, f'button_{curr_mode}')
        button.background_color = [255 / 255, 235 / 255, 204 / 255, 1]
        button.color = [0, 0, 0, 1]

        self.current_mode = self.modes[to_mode]
        button = getattr(ids, f'button_{to_mode}')
        button.background_color = [54/255, 48/255, 115/255, 1]
        button.color = [1, 1, 1, 1]

        if rerun:
            self.values = None
            self.run()

    def run(self):
        if not self.start_time:
            self.start_time = datetime.now()

        self.base.nav_drawer.set_state('close')
        # self.base.screen.ids.action_bar.title = 'Schulte Table'

        self.change_version(self.version)

        # RUN VERSION AND MODE
        self.create_table()

        self.base.manager.current = 'schulte_table'
        self.base.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.base.back_screen(27)]]
