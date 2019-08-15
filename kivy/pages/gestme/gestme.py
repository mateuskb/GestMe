import sys, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

BASE_PATH = os.path.abspath(__file__+ '/../../../')

sys.path.append(BASE_PATH)
from inc.consts.consts import Consts

# Load KV file
Builder.load_file(BASE_PATH + '/pages/gestme/gestme.kv')

class GestMeWindow(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def consts(self):
        return Consts()

    def redirect_login(self):
        self.parent.parent.current = 'login_screen'

    def redirect_signup(self):
        self.parent.parent.current = 'signup_screen'

class GestMeApp(App):

    def build(self):
        return GestMeWindow()

if __name__ == '__main__':
    GestMeApp().run()