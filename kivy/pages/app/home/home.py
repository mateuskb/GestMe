import sys, os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel

from kivy.clock import Clock
import pandas as pd

BASE_PATH = os.path.abspath(__file__+ '/../../../../')

sys.path.append(BASE_PATH)
from inc.classes.Buttons import HoverButton, ImageButton
from inc.classes.Requests import Requests
from inc.classes.Storage import Storage
from inc.consts.consts import Consts


# Load KV file
Builder.load_file(BASE_PATH + '/pages/app/home/home.kv')


class HomeWindow(Screen):
    
    def __init__(self, **kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        # Check for login
        auth_token = Storage.r_authtoken()
        if not auth_token:
            Clock.schedule_once(self.logout, 2/30)

    def consts(self):
        return Consts()

    def logout(self):
        resp = Storage.logoff()
        if resp:
            App.get_running_app().unload_app()


class HomeApp(App):

    def build(self):
        return HomeWindow()

if __name__ == '__main__':
    HomeApp().run()
