import sys, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


BASE_PATH = os.path.abspath(__file__+ '/../../../')

sys.path.append(BASE_PATH)
from inc.consts.consts import Consts
from inc.classes.Storage import Storage

# Load KV file
Builder.load_file(BASE_PATH + '/pages/gestme/gestme.kv')

class GestMeWindow(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        resp = Storage.r_authtoken()
        if resp:
            Clock.schedule_once(self.redirect_app_app, 2/60) # Already logged in
        
    def consts(self):
        return Consts()

    def redirect_login(self):
        self.parent.current = 'login_screen'

    def redirect_signup(self):
        self.parent.current = 'signup_screen'

    def redirect_app_app(self, dt):
        App.get_running_app().load_app()
        self.parent.current = 'app_app_screen'

class GestMeApp(App):

    def build(self):
        return GestMeWindow()

if __name__ == '__main__':
    GestMeApp().run()