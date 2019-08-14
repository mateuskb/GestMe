import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

sys.path.append('../../')
from inc.classes.Requests import Requests
from inc.consts.consts import Consts

# Load KV file
Builder.load_file('pages/signup/signupok.kv')

class SignupokWindow(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def consts(self):
        return Consts()
    
    def redirect_main(self):
        self.parent.parent.current = 'gestme_screen'

    def redirect_forgetpw(self):
        pass


class SignupokApp(App):

    def build(self):
        return SignupokWindow()

if __name__ == '__main__':
    SignupokApp().run()
