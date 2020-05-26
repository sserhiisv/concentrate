# -*- coding: utf-8 -*-

import os
import sys
import random

from datetime import datetime
from ast import literal_eval

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.logger import PY2
from kivy.clock import Clock
from kivy.utils import get_hex_from_color
from kivy.properties import ObjectProperty, StringProperty


from main import __version__
from libs.translation import Translation
from libs.uix.baseclass.startscreen import StartScreen
from libs.uix.lists import Lists

from kivymd.app import MDApp
from kivymd.toast import toast

from dialogs import card

from libs.strategy.schulte_table import SchulteTableCore
from libs.strategy.twins import Twins


class PyConversations(MDApp):
    title = 'App'
    icon = 'brain.png'
    nav_drawer = ObjectProperty()
    lang = StringProperty('en')

    def __init__(self, **kvargs):
        super(PyConversations, self).__init__(**kvargs)
        Window.bind(on_keyboard=self.events_program)
        Window.soft_input_mode = 'below_target'

        # self.admob_id = 'ca-app-pub-8865711525352558~2442322860'
        # self.banner_id = ''
        # self.interstitial_id = ''
        # self.ads = KivMob(self.admob_id)

        self.list_previous_screens = ['base']
        self.window = Window
        self.config = ConfigParser()
        self.manager = None
        self.window_language = None
        self.exit_interval = False
        self.dict_language = literal_eval(
            open(
                os.path.join(self.directory, 'data', 'locales', 'locales.txt')).read()
        )
        self.translation = Translation(
            self.lang, 'Ttest', os.path.join(self.directory, 'data', 'locales')
        )

        self.start_time = None

    def get_application_config(self):
        return super(PyConversations, self).get_application_config(
                        '{}/%(appname)s.ini'.format(self.directory))

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'language', 'en')

    def set_value_from_config(self):
        self.config.read(os.path.join(self.directory, 'pyconversations.ini'))
        self.lang = self.config.get('General', 'language')

    def build(self):
        self.set_value_from_config()
        self.load_all_kv_files(os.path.join(self.directory, 'libs', 'uix', 'kv'))
        self.screen = StartScreen()
        self.manager = self.screen.ids.manager
        self.nav_drawer = self.screen.ids.nav_drawer

        return self.screen

    def load_all_kv_files(self, directory_kv_files):
        for kv_file in os.listdir(directory_kv_files):
            kv_file = os.path.join(directory_kv_files, kv_file)
            if os.path.isfile(kv_file):
                if not PY2:
                    with open(kv_file, encoding='utf-8') as kv:
                        Builder.load_string(kv.read())
                else:
                    Builder.load_file(kv_file)

    def events_program(self, instance, keyboard, keycode, text, modifiers):

        if keyboard in (1001, 27):
            if self.nav_drawer.state == 'open':
                self.nav_drawer.toggle_nav_drawer()
            self.back_screen(event=keyboard)
        elif keyboard in (282, 319):
            pass

        return True

    def back_screen(self, event=None):
        if event in (1001, 27):
            if self.manager.current == 'base':
                self.dialog_exit()
                return
            try:
                self.manager.current = self.list_previous_screens.pop()
            except:
                self.manager.current = 'base'
            # self.screen.ids.action_bar.title = self.title
            self.screen.ids.action_bar.left_action_items = \
                [['menu', lambda x: self.nav_drawer.toggle_nav_drawer()]]

    def show_pair_screen(self, *args):
        self.twins = Twins(self)
        self.twins.run()

    def schulte_table_screen(self, *args):
        self.nav_drawer.set_state('close')
        self.manager.current = 'schulte_table_type'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]

    def run_schulte_table(self, version):
        self.schulte_table = SchulteTableCore(self, version)
        self.schulte_table.run()

    # def get_banner(self):
    #     self.ads.new_banner(self.banner_id, top_pos=True)
    #     self.ads.request_banner()
    #     self.ads.show_banner()
    #
    # def get_interstitial(self):
    #     self.ads.new_interstitial(self.interstitial_id)
    #     self.ads.request_interstitial()
    #     self.ads.show_banner()
    #     return Button(text='Show Interstitial',
    #                   on_release=lambda a: self.ads.show_interstitial())

    # def show_end_game(self, *args):
    #     from collections import OrderedDict
    #ї
    #     from kivy.storage.jsonstore import JsonStore
    #
    #     self.stored_data = JsonStore('data/results/data.json')
    #     self.nav_drawer.set_state('close')
    #     # self.screen.ids.tryagain.ids.label.text = 'Find The Twins'
    #
    #     # total_time = datetime.now() - self.start_time
    #     total_time_str = f'{22}:{78}'
    #     self.screen.ids.tryagain.ids.label_result.text = total_time_str
    #
    #     data = list(OrderedDict(self.stored_data))
    #
    #     if len(data) > 5:
    #         data = data[:5]
    #
    #     self.version = 'numbers'
    #
    #     self.NUMBERS = 0
    #     self.LETTERS = 1
    #     self.versions = {
    #         'numbers': self.NUMBERS,
    #         'letters': self.LETTERS
    #     }
    #
    #     self.current_version = self.NUMBERS
    #
    #     self.DYNAMIC = 0
    #     self.STATIC = 1
    #     self.modes = {
    #         'dynamic': self.DYNAMIC,
    #         'static': self.STATIC
    #     }
    #     self.current_mode = self.DYNAMIC
    #
    #     self.LOWER = 0
    #     self.UPPER = 1
    #     self.MIXED = 2
    #     self.cases = {
    #         'lower': self.LOWER,
    #         'upper': self.UPPER,
    #         'mixed': self.MIXED
    #     }
    #     self.current_case = self.LOWER
    #
    #     for el in data:
    #         x = self.stored_data.get(el)
    #         case = list(self.cases.keys())[
    #             list(self.cases.values()).index(x.get("case"))]
    #         mode = list(self.modes.keys())[
    #             list(self.modes.values()).index(x.get("mode"))]
    #
    #         ids = self.screen.ids.tryagain.ids
    #         label = getattr(ids, f'result_{str(data.index(el)+1)}')
    #         label.text = f'{x.get("version")} / {case} / {mode} - {x.get("time")}'
    #
    #     # button = self.screen.ids.tryagain.ids.start
    #     # button.on_press = self.run
    #     self.manager.current = 'tryagain'
