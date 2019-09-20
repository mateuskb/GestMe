import sys, os, webbrowser
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
import pandas as pd

BASE_PATH = os.path.abspath(__file__+ '/../../../../')

sys.path.append(BASE_PATH)
from inc.classes.Buttons import HoverButton, ImageButton
from inc.classes.Requests import Requests
from inc.classes.Storage import Storage
from inc.consts.consts import Consts


# Load KV file
Builder.load_file(BASE_PATH + '/pages/app/update_perfil/uperfil.kv')


class UperfilWindow(Screen):

    avatar = BASE_PATH + '/inc/assets/avatars/default.png'

    def __init__(self, **kwargs):
        super(UperfilWindow, self).__init__(**kwargs)
        # Check for login
        self.auth_token = Storage.r_authtoken()
        if not self.auth_token:
            Clock.schedule_once(self.logout, 2/30)
        else:
            Clock.schedule_once(self.load_profile, 3/30)
        
    def load_profile(self, dt):
        resp = Requests.r_perfil()
        if resp:
            if resp['status'] == 200:
                perfil = resp['data'] if 'data' in resp else []
                
            else:
                self.logout()
        else:
            self.logout()
        
    def consts(self):
        return Consts()
        
    def redirect_app_home(self):
        self.parent.current = 'app_home_screen'

    def logout(self):
        resp = Storage.logoff()
        if resp:
            App.get_running_app().unload_app()


class UperfilApp(App):

    def build(self):
        return UperfilWindow()

if __name__ == '__main__':
    UperfilApp().run()
