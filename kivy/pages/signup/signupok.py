import sys, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


BASE_PATH = os.path.abspath(__file__+ '/../../../')

sys.path.append(BASE_PATH)
from inc.classes.Requests import Requests
from inc.consts.consts import Consts

# Load KV file
Builder.load_file(BASE_PATH + '/pages/signup/signupok.kv')

class SignupokWindow(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def consts(self):
        return Consts()
    
    def redirect_main(self):
        self.parent.current = 'gestme_screen'


class SignupokApp(App):

    def build(self):
        return SignupokWindow()

if __name__ == '__main__':
    SignupokApp().run()
