import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

sys.path.append('../../')
from inc.Classes.Requests import Requests
from consts.consts import Consts

# Load KV file
Builder.load_file('pages/signup/signup.kv')

class SignUpWindow(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def consts(self):
        return Consts()

    def redirect_gestme(self):
        self.parent.parent.current = 'gestme_screen'
        


class SignUpApp(App):

    def build(self):
        return SignUpWindow()

if __name__ == '__main__':
    SignUpApp().run()