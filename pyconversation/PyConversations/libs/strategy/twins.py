import random

import time

from datetime import datetime
from collections import OrderedDict

from kivy.storage.jsonstore import JsonStore

from vars import ICONS


class Twins:

    def __init__(self, base):
        self.base = base
        self.start_time = None
        self.stored_data = JsonStore('data/results/data.json')

        self.colored = True

    def show_end_game(self, won_count, win_count):
        self.base.nav_drawer.set_state('close')

        total_time = datetime.now() - self.start_time
        total_time_str = f'{won_count} of {win_count} | {(total_time.seconds % 3600) // 60}:{total_time.seconds % 60}'
        self.base.screen.ids.tryagain.ids.label_result.text = total_time_str

        self.stored_data.put(
            int(time.time()),
            mode=self.colored,
            time=total_time_str
        )

        data = list(OrderedDict(self.stored_data))
        if len(data) > 5:
            data = data[:5]

        # for el in data:
        #     x = self.stored_data.get(el)
            # mode = list(self.modes.keys())[
            #     list(self.modes.values()).index(x.get("mode"))]

            # ids = self.base.screen.ids.tryagain.ids
            # label = getattr(ids, f'result_{str(data.index(el)+1)}')
            # label.text = f'{self.colored} - {x.get("time")}'

        label = getattr(self.base.screen.ids.tryagain.ids, f'result_5')
        label.text = '⭐' * won_count
        label.color = [54 / 255, 48 / 255, 115 / 255, 1]
        label.font_name = "data/fonts/NotoEmoji-Regular.ttf"
        label.font_size = self.base.screen.ids.tryagain.ids.start.font_size

        button = self.base.screen.ids.tryagain.ids.start
        button.on_press = self.run
        self.base.manager.current = 'tryagain'

    def handle_result(self, result):
        if result.get('win_count') and result.get('attempts'):
            if result.get('win_count') == result.get('attempts'):
                self.show_end_game(result.get('won_count'), result.get('win_count'))
            elif result.get('finish'):
                self.show_end_game(result.get('won_count'), result.get('win_count'))
            elif result.get('check') and not result.get('finish'):
                self.run()

    def change_color(self, to_color, rerun=False):
        ids = self.base.screen.ids.pair.ids

        curr_case = 'color' if self.colored else 'bw'
        button = getattr(ids, f'button_{curr_case}')
        button.background_color = [255 / 255, 235 / 255, 204 / 255, 1]
        button.color = [0, 0, 0, 1]

        self.colored = to_color
        button = getattr(ids, f'button_{"color" if to_color else "bw"}')
        button.background_color = [54 / 255, 48 / 255, 115 / 255, 1]
        button.color = [1, 1, 1, 1]

        if rerun:
            self.run()

    def run(self):
        self.base.nav_drawer.set_state('close')
        self.base.screen.ids.action_bar.title = 'Find The Twins'

        if not self.start_time:
            self.start_time = datetime.now()

        values = ICONS.copy()

        double_icon = random.choice(values)
        values.append(double_icon)
        random.shuffle(values)

        for el in range(1, 26):
            pair_ids = self.base.screen.ids.pair.ids
            source = f'button_{el}'
            button = getattr(pair_ids, source)
            elem = values.pop()
            button.text = elem['icon']
            button.background_color = [255 / 255, 235 / 255, 204 / 255, 1]
            if self.colored:
                button.color = elem['color']
            else:
                button.color = [0, 0, 0, 1]
            button.font_name = "data/fonts/NotoEmoji-Regular.ttf"

        self.base.manager.current = 'pair'
        self.base.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.base.back_screen(27)]]
